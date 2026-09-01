#!/usr/bin/env python3
"""Export cookies for one domain out of macOS Chrome, decrypted.

`browse cookie-import-browser chrome --domain medium.com` looks like it works but
silently skips every encrypted value, so you end up importing only the throwaway
plaintext cookies and stay logged out. This reads the profile's SQLite store
directly and decrypts the `v10` values itself.

Usage:
    python3 tools/chrome_cookies.py medium.com --list
    python3 tools/chrome_cookies.py medium.com --profile Default --out /tmp/medium.json

Then hand the file to browse, and delete it afterwards:
    browse --headed cookie-import "$OUT" && rm -f "$OUT"

macOS only: it reads the key from the login keychain via `security` and
decrypts with `openssl`.
"""

import argparse
import binascii
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile

CHROME_DIR = os.path.expanduser("~/Library/Application Support/Google/Chrome")
SAME_SITE = {0: "None", 1: "Lax", 2: "Strict", -1: "Lax"}

PBKDF2_ITERATIONS = 1003          # Chrome's fixed count on macOS
AES_KEY_BYTES = 16
AES_BLOCK_BYTES = 16
DOMAIN_HASH_PREFIX = 32           # newer Chrome prepends sha256(domain)
WEBKIT_EPOCH_OFFSET_S = 11644473600
MICROS_PER_S = 1000000


def safe_storage_key():
    """The AES password Chrome stashes in the login keychain.

    Reading it may pop a keychain prompt the first time; approve it once and the
    grant sticks.
    """
    out = subprocess.run(
        ["security", "find-generic-password", "-w",
         "-s", "Chrome Safe Storage", "-a", "Chrome"],
        capture_output=True, text=True,
    )
    if out.returncode != 0 or not out.stdout.strip():
        sys.exit("could not read 'Chrome Safe Storage' from the keychain: "
                 + out.stderr.strip())
    return out.stdout.strip().encode()


def decrypt(blob, hexkey, hexiv, host=None):
    """Decrypt one v10 cookie, or return None if it cannot be read.

    Known trade-off: the key goes to openssl in argv, so it is visible in the
    process list to any same-uid process for the life of the call. That is the
    same trust boundary as the keychain read that produced it, and the
    alternative (a pure-Python AES) is a lot of hand-rolled crypto to avoid a
    window an attacker at that privilege level can already step around.
    """
    if not blob or blob[:3] != b"v10":
        return None
    proc = subprocess.run(
        ["openssl", "enc", "-aes-128-cbc", "-d",
         "-K", hexkey, "-iv", hexiv, "-nopad"],
        input=blob[3:], capture_output=True,
    )
    if proc.returncode != 0 or not proc.stdout:
        return None
    dec = proc.stdout
    pad = dec[-1]
    # Validate the whole PKCS7 pad, not just the last byte: noise from a wrong
    # key routinely ends in a plausible-looking length.
    if 1 <= pad <= AES_BLOCK_BYTES and dec[-pad:] == bytes([pad]) * pad:
        dec = dec[:-pad]
    if host is not None:
        # Newer Chrome prefixes the plaintext with sha256(host_key). Checking it
        # beats guessing from a failed decode, which silently kept 32 bytes of
        # hash on the front whenever they happened to be valid UTF-8.
        digest = hashlib.sha256(host.encode()).digest()
        if dec.startswith(digest):
            dec = dec[len(digest):]
    if not dec:
        # A wrong key decrypts to noise whose last byte often reads as a full
        # block of padding, unpadding to nothing. That is a failure, not a
        # cookie with an empty value.
        return None
    try:
        return dec.decode("utf-8") or None
    except UnicodeDecodeError:
        pass
    if len(dec) > DOMAIN_HASH_PREFIX:
        try:
            # Newer Chrome prefixes the plaintext with a 32-byte domain hash.
            return dec[DOMAIN_HASH_PREFIX:].decode("utf-8") or None
        except UnicodeDecodeError:
            pass
    # A stale keychain key decrypts to noise. Returning a mangled or empty
    # string here would export a cookie that looks fine and silently fails to
    # authenticate, which is the exact failure this tool exists to avoid.
    return None


def profiles():
    if not os.path.isdir(CHROME_DIR):
        sys.exit("no Chrome profile directory at " + CHROME_DIR)
    found = []
    for entry in sorted(os.listdir(CHROME_DIR)):
        if os.path.isfile(os.path.join(CHROME_DIR, entry, "Cookies")):
            found.append(entry)
    return found


def read_profile(profile, domain, hexkey, hexiv, subdomains=False):
    """Cookies for `domain`.

    By default this keeps only `domain` and `.domain`. `browse cookie-import`
    refuses any cookie whose domain is not a suffix of the page you are on, so
    stray per-subdomain cookies (fantasybz.medium.com, picked up by reading a
    published post) make the whole import fail.

    `subdomains=True` widens to real subdomains only. The SQL LIKE is a cheap
    prefilter and is not a host match on its own: `%medium.com` also matches
    notmedium.com, so the host boundary is always checked in Python.
    """
    src = os.path.join(CHROME_DIR, profile, "Cookies")
    # Chrome holds a lock on the live database, so work off a copy.
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    shutil.copy(src, tmp.name)
    try:
        con = sqlite3.connect(tmp.name)
        try:
            rows = con.execute(
                "select host_key, name, encrypted_value, value, path, expires_utc,"
                " is_secure, is_httponly, samesite from cookies"
                " where host_key like ?", ("%" + domain,),
            ).fetchall()
        finally:
            con.close()
    finally:
        os.unlink(tmp.name)

    exact = {domain, "." + domain}
    cookies = []
    for host, name, enc, val, path, exp, secure, httponly, samesite in rows:
        if host in exact:
            pass
        elif subdomains and host.lstrip(".").endswith("." + domain):
            pass
        else:
            continue
        value = val if val else decrypt(enc, hexkey, hexiv, host)
        if value is None:
            continue
        expires = exp / MICROS_PER_S - WEBKIT_EPOCH_OFFSET_S if exp else -1
        cookies.append({
            "name": name,
            "value": value,
            "domain": host,
            "path": path,
            "expires": expires if expires > 0 else -1,
            "httpOnly": bool(httponly),
            "secure": bool(secure),
            "sameSite": SAME_SITE.get(samesite, "Lax"),
        })
    return cookies


def write_private(path, cookies):
    """Create the file owner-only, before anything secret is in it.

    A plain open() + chmod writes the session at the umask default first and
    narrows it afterwards, and follows a symlink an attacker pre-created at a
    predictable path. O_EXCL|O_NOFOLLOW closes both.
    """
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
    try:
        fd = os.open(path, flags, 0o600)
    except FileExistsError:
        sys.exit("refusing to overwrite %s — delete it first" % path)
    with os.fdopen(fd, "w") as fh:
        json.dump(cookies, fh)


def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("domain", help="cookie domain, e.g. medium.com")
    ap.add_argument("--profile", help="Chrome profile directory name (default: pick one)")
    ap.add_argument("--out", help="write the cookie JSON here")
    ap.add_argument("--list", action="store_true",
                    help="show what each profile holds and exit")
    ap.add_argument("--subdomains", action="store_true",
                    help="also include cookies scoped to subdomains")
    args = ap.parse_args()

    key = safe_storage_key()
    hexkey = binascii.hexlify(hashlib.pbkdf2_hmac(
        "sha1", key, b"saltysalt", PBKDF2_ITERATIONS, AES_KEY_BYTES)).decode()
    hexiv = binascii.hexlify(b" " * AES_BLOCK_BYTES).decode()

    available = profiles()
    if not available:
        sys.exit("no Chrome profile has a Cookies database")

    wanted = [args.profile] if args.profile else available
    results = {}
    for profile in wanted:
        if profile not in available:
            sys.exit("no such profile: %s (have: %s)" % (profile, ", ".join(available)))
        results[profile] = read_profile(profile, args.domain, hexkey, hexiv,
                                        subdomains=args.subdomains)

    if args.list or not args.profile:
        for profile, cookies in results.items():
            names = {c["name"]: c["value"] for c in cookies}
            uid = names.get("uid", "")
            # Medium hands logged-out visitors a uid prefixed with "lo_".
            state = "logged out" if uid.startswith("lo_") else ("logged in" if uid else "no uid")
            print("%-12s %2d cookies  %s" % (profile, len(cookies), state))
        if args.list:
            return
        sys.exit("\npick one with --profile <name> --out <path>")

    cookies = results[args.profile]
    if not cookies:
        sys.exit("profile %s has no cookies for %s" % (args.profile, args.domain))
    out = args.out or os.path.join(
        tempfile.mkdtemp(prefix="cookies-"),
        "%s-cookies.json" % args.domain.replace(".", "-"))
    write_private(out, cookies)
    print("wrote %d cookies to %s" % (len(cookies), out))
    print("this file is a live session — delete it when the import is done")


if __name__ == "__main__":
    main()
