"""Export the Notion desktop app's cookies for one domain, decrypted.

The Notion app is Electron, so its cookie store is the same Chromium SQLite + v10
AES scheme that tools/chrome_cookies.py already handles; only the keychain item
("Notion Safe Storage" / account "Notion Key") and the directory differ. This
reuses that module rather than copying the crypto.

    python3 research/scripts/notion_cookies.py notion.com "$W/ncom.json"
    python3 research/scripts/notion_cookies.py notion.so  "$W/nso.json"

The first run pops a Keychain prompt that a human has to approve; an unattended
run blocks there until it times out (that is what happened on 2026-09-05 01:16;
approved at 10:47 the same day). Verified: the export includes token_v2 (scoped
to app.notion.com) and logs the headed browser in, provided the cookies are
imported in two batches from the matching domains — see collect.sh do_notion.
"""
import binascii
import hashlib
import importlib.util
import os
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
spec = importlib.util.spec_from_file_location("cc", os.path.join(ROOT, "tools", "chrome_cookies.py"))
cc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cc)

cc.CHROME_DIR = os.path.expanduser("~/Library/Application Support/Notion/Partitions")


def notion_key():
    out = subprocess.run(
        ["security", "find-generic-password", "-w", "-s", "Notion Safe Storage", "-a", "Notion Key"],
        capture_output=True, text=True,
    )
    if out.returncode != 0 or not out.stdout.strip():
        sys.exit("could not read 'Notion Safe Storage' from the keychain: " + out.stderr.strip())
    return out.stdout.strip().encode()


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: notion_cookies.py <domain> <out.json>")
    dom, outpath = sys.argv[1], sys.argv[2]
    key = notion_key()
    hexkey = binascii.hexlify(hashlib.pbkdf2_hmac(
        "sha1", key, b"saltysalt", cc.PBKDF2_ITERATIONS, cc.AES_KEY_BYTES)).decode()
    hexiv = binascii.hexlify(b" " * cc.AES_BLOCK_BYTES).decode()
    cookies = cc.read_profile("notion", dom, hexkey, hexiv, subdomains=True)
    print(dom, "->", len(cookies), "cookies:", sorted(set(c["name"] for c in cookies)))
    if not cookies:
        sys.exit("no cookies for " + dom)
    cc.write_private(outpath, cookies)
    print("this file is a live session — delete it when the import is done")


if __name__ == "__main__":
    main()
