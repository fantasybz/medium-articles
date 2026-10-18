"""Fail-closed macOS evaluator boundary; generated code never sees the oracle.

This is an execution boundary for a local controlled study, not a general
container service. Only the sealed candidate and Python runtime are readable.
No credentials, network, writable directories, or oracle files are exposed.
"""
from dataclasses import dataclass
import json
import os
from pathlib import Path
import platform
import resource
import select
import signal
import subprocess
import sys
import tempfile
import time


class SandboxUnavailable(RuntimeError):
    pass


@dataclass(frozen=True)
class CandidateRun:
    returncode: int
    stdout: str
    stderr: str
    timed_out: bool
    sandbox: str = "macos-seatbelt-v1"


def profile(candidate: Path) -> str:
    if platform.system() != "Darwin" or not Path("/usr/bin/sandbox-exec").is_file():
        raise SandboxUnavailable("This release requires macOS sandbox-exec; no unsandboxed fallback")
    runtime = Path(sys.base_prefix).resolve()
    exe = Path(sys.executable).resolve()
    # A system Python would accidentally grant /usr; require a dedicated runtime.
    if runtime in (Path("/"), Path("/usr"), Path("/usr/local"), Path("/opt/homebrew")):
        raise SandboxUnavailable("Use a Python installation with a dedicated runtime directory")
    literal = lambda p: json.dumps(str(p))
    return "\n".join([
        "(version 1)", "(deny default)",
        "(allow process-exec)", "(allow sysctl-read)", "(allow mach-lookup)",
        "(allow file-read-metadata)",
        f"(allow file-read* (literal {literal(candidate)}) (literal {literal(exe)})",
        f"  (subpath {literal(runtime)}) (subpath \"/System/Library\")",
        "  (subpath \"/usr/lib\") (literal \"/\") (literal \"/dev/null\")",
        "  (literal \"/dev/random\") (literal \"/dev/urandom\"))",
    ])


def run_candidate(candidate_dir: Path, request: str, *, timeout_seconds: float = 3.0,
                  max_output_bytes: int = 65536, script_name: str = "codex_jsonl.py",
                  c_locale: bool = False) -> CandidateRun:
    if script_name not in ("codex_jsonl.py", "probe.py"):
        raise ValueError("Candidate filename is outside the allowlist")
    original = Path(candidate_dir) / script_name
    if original.is_symlink() or not original.is_file():
        raise SandboxUnavailable("Candidate must be a regular file, never a symlink")
    candidate = original.resolve()
    policy = profile(candidate)
    if timeout_seconds <= 0 or max_output_bytes <= 0:
        raise ValueError("Positive time and output limits required")

    def limits():
        resource.setrlimit(resource.RLIMIT_CPU, (max(1, int(timeout_seconds)), max(2, int(timeout_seconds) + 1)))
        resource.setrlimit(resource.RLIMIT_FSIZE, (max_output_bytes, max_output_bytes))
        resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))

    with tempfile.TemporaryFile() as out, tempfile.TemporaryFile() as err:
        environment = {"PATH": "/usr/bin:/bin", "LANG": "en_US.UTF-8"}
        if c_locale:
            environment.update(LC_ALL="C", LANG="C", PYTHONIOENCODING="", PYTHONUTF8="0")
        proc = subprocess.Popen([
            "/usr/bin/sandbox-exec", "-p", policy, str(Path(sys.executable).resolve()),
            "-I", "-B", *(["-X", "utf8=0"] if c_locale else []), str(candidate),
        ], cwd=candidate.parent, stdin=subprocess.PIPE, stdout=out, stderr=err,
            env=environment,
            start_new_session=True, preexec_fn=limits)
        timed_out = False
        try:
            proc.communicate(request.encode(), timeout=timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            os.killpg(proc.pid, signal.SIGKILL)
            proc.communicate()
        out.seek(0)
        err.seek(0)
        stdout = out.read(max_output_bytes + 1).decode("utf-8", errors="replace")
        stderr = err.read(max_output_bytes + 1).decode("utf-8", errors="replace")
    return CandidateRun(proc.returncode, stdout, stderr, timed_out)


def preflight() -> dict:
    """Prove ordinary execution works AND oracle reads/writes/network are denied."""
    with tempfile.TemporaryDirectory(prefix="variance-probe-") as directory:
        root = Path(directory)
        candidate = root / "candidate"
        candidate.mkdir()
        secret = root / "oracle-canary.txt"
        secret.write_text("DO_NOT_EXPOSE_ORACLE")
        probe = '''import json, socket, pathlib
results = {}
try:
    pathlib.Path(SECRET).read_text(); results['read_denied'] = False
except PermissionError:
    results['read_denied'] = True
try:
    pathlib.Path(WRITE).write_text('forbidden'); results['write_denied'] = False
except PermissionError:
    results['write_denied'] = True
try:
    s = socket.socket(); s.bind(('127.0.0.1', 0)); results['network_denied'] = False
except PermissionError:
    results['network_denied'] = True
print(json.dumps(results))
'''.replace("SECRET", repr(str(secret))).replace("WRITE", repr(str(candidate / "forbidden")))
        (candidate / "probe.py").write_text(probe)
        result = run_candidate(candidate, "", script_name="probe.py")
        try:
            observed = json.loads(result.stdout)
        except (ValueError, TypeError) as exc:
            raise SandboxUnavailable(f"Sandbox execution probe failed: {result.stderr[:500]}") from exc
        expected = {"read_denied": True, "write_denied": True, "network_denied": True}
        if result.returncode != 0 or result.timed_out or observed != expected:
            raise SandboxUnavailable(f"Sandbox isolation probe failed: {observed}")
        return {"sandbox": result.sandbox, **observed}


def run_streaming_probe(candidate_dir: Path, prefix: str, suffix: str,
                        expected_prefix: str, *, timeout_seconds: float = 3.0) -> dict:
    """Observe a message before sending the terminal event or closing stdin."""
    candidate = Path(candidate_dir) / "codex_jsonl.py"
    if candidate.is_symlink() or not candidate.is_file():
        raise SandboxUnavailable("Candidate must be a regular file")
    candidate = candidate.resolve()
    proc = subprocess.Popen([
        "/usr/bin/sandbox-exec", "-p", profile(candidate), str(Path(sys.executable).resolve()),
        "-I", "-B", str(candidate),
    ], cwd=candidate.parent, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL, env={"PATH": "/usr/bin:/bin", "LANG": "en_US.UTF-8"},
        start_new_session=True)
    early = b""
    expected = expected_prefix.encode()
    try:
        proc.stdin.write(prefix.encode())
        proc.stdin.flush()
        deadline = time.monotonic() + timeout_seconds
        while len(early) < len(expected) and len(early) < 65536:
            remaining = deadline - time.monotonic()
            if remaining <= 0 or not select.select([proc.stdout], [], [], remaining)[0]:
                break
            chunk = os.read(proc.stdout.fileno(), min(4096, 65536 - len(early)))
            if not chunk:
                break
            early += chunk
        observed_before_eof = early == expected and proc.poll() is None
        if proc.poll() is None:
            proc.stdin.write(suffix.encode())
            proc.stdin.flush()
            proc.stdin.close()
            proc.stdin = None
            # Drain without unbounded communicate() buffering.
            deadline = time.monotonic() + timeout_seconds
            while proc.poll() is None:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                if select.select([proc.stdout], [], [], min(remaining, 0.05))[0]:
                    os.read(proc.stdout.fileno(), 4096)
        return {"passed": observed_before_eof and proc.poll() == 0,
                "observed_before_eof": observed_before_eof,
                "early_stdout": early.decode("utf-8", errors="replace"),
                "returncode": proc.poll(), "sandbox": "macos-seatbelt-v1"}
    except BrokenPipeError:
        return {"passed": False, "observed_before_eof": False, "returncode": proc.poll(),
                "sandbox": "macos-seatbelt-v1"}
    finally:
        if proc.poll() is None:
            os.killpg(proc.pid, signal.SIGKILL)
            proc.wait()
        if proc.stdin is not None:
            try:
                proc.stdin.close()
            except BrokenPipeError:
                pass
        proc.stdout.close()


if __name__ == "__main__":
    print(json.dumps(preflight(), indent=2))
