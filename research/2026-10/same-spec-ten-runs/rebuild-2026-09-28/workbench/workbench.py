#!/usr/bin/env python3
"""執行可信 parser fixture 的契約教學；不是正式研究評分器或沙箱。"""

from __future__ import annotations

import argparse
import ast
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import queue
import re
import subprocess
import sys
import tempfile
import threading
import time


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
SOURCE = REPO / "research/experiments/same-spec-ten-runs/results/formal-2026-09-25/source"
PINNED = {
    "tests/fixtures/parser_reference.py": "aad3638eecf746ee473893d805e0734f68dd2a861f4de25be7831da390db1c9f",
    "tests/test_task_evaluator.py": "e6ff5eaa2fa043aa4a95a1fadf32bab7df7cc388905b9d81912278a05e82c952",
    "requirements.json": "32e0a0af2578564624b5a5b5f9d981e0dc296e6eb690b6598482cb809419a515",
    "evaluator.py": "443b47cc93ca1559293a6025472696eee8351a25cb8486e09ee682bcfd29508a",
}
TOKENS = "\n<!-- tokens: in 10 out 5 -->\n"
FAILED = "[codex] the turn failed (reason above); no review was produced.\n"
DONE = {"type": "turn.completed", "usage": {"input_tokens": 10, "output_tokens": 5}}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def verify_sources() -> dict:
    rows = {}
    for relative, expected in PINNED.items():
        actual = sha256((SOURCE / relative).read_bytes())
        if actual != expected:
            raise RuntimeError(f"凍結來源 SHA 不符，停止教學：{relative}")
        rows[str((SOURCE / relative).relative_to(REPO))] = actual
    return rows


def message(text):
    return {"type": "item.completed", "item": {"type": "agent_message", "text": text}}


def jsonl(*events) -> str:
    return "".join(json.dumps(event, ensure_ascii=False) + "\n" for event in events)


@dataclass(frozen=True)
class Expected:
    stdout: str
    stderr: tuple[str | int, ...]
    returncode: int


@dataclass(frozen=True)
class Case:
    name: str
    requirements: tuple[str, ...]
    input_text: str
    expected: Expected


@dataclass(frozen=True)
class Observed:
    stdout: str
    stderr: str
    returncode: int


def stderr_pattern(parts: tuple[str | int, ...]) -> str:
    # int 表示 malformed 的實體行號；REASON 不得固定成 reference 的用字。
    return "".join(
        re.escape(f"[codex malformed event] line {part}: ") + r"[^\r\n]+\n"
        if isinstance(part, int) else re.escape(part)
        for part in parts
    )


def grade(expected: Expected, observed: Observed) -> dict:
    channels = {
        "stdout": observed.stdout == expected.stdout,
        "stderr": re.fullmatch(stderr_pattern(expected.stderr), observed.stderr) is not None,
        "returncode": observed.returncode == expected.returncode,
    }
    return {"passed": all(channels.values()), "channels": channels,
            "mismatches": [key for key, value in channels.items() if not value]}


def cases() -> tuple[Case, ...]:
    return (
        Case("happy", ("R05", "R08", "R11"), jsonl(message("ok"), DONE),
             Expected("ok\n" + TOKENS, (), 0)),
        Case("false-text", ("R03", "R05", "R08", "R11"),
             jsonl(message(False), message("after"), DONE),
             Expected("after\n" + TOKENS, (1,), 6)),
        Case("continue-after-malformed", ("R02", "R03", "R05", "R08", "R11"),
             jsonl([], message("after"), DONE),
             Expected("after\n" + TOKENS, (1,), 6)),
        Case("explicit-failure-priority", ("R03", "R09", "R11", "R12"),
             jsonl([], {"type": "error", "message": "refused"}, message("after"), DONE),
             Expected("after\n" + TOKENS, (1, "[codex error] refused\n", FAILED), 3)),
    )


# 已知的單點錯法；來源與唯一 replacement anchor 一起存進結果供查核。
# 不接收外部 candidate、模型輸出或自行提供的程式。
MUTATIONS = (
    {
        "name": "coerce-nontext",
        "purpose": "把非字串轉成文字；false 被印成 False，R05 遭到改變。",
        "origin": "凍結 test_task_evaluator.py 的 coerce-nontext-agent 變異方式；改用 false 作教學輸入。",
        "before": 'raise MalformedEvent(field + " must be a string or null")',
        "after": "return str(value)",
        "witness": "false-text",
        "expected_mismatches": ["stdout", "stderr", "returncode"],
    },
    {
        "name": "false-as-absent",
        "purpose": "用 Python 真假值判斷，把 false 靜默當作沒有訊息。",
        "origin": "依 R05 自寫的教學錯法；不是正式候選。",
        "before": 'if value is None or value == "":',
        "after": "if not value:",
        "witness": "false-text",
        "expected_mismatches": ["stderr", "returncode"],
    },
    {
        "name": "stop-after-malformed",
        "purpose": "遇到壞事件就結束，漏處理後續有效訊息與完成事件。",
        "origin": "凍結 test_task_evaluator.py 的 stop-reading-after-malformed 變異方式。",
        "before": "        except MalformedEvent as exc:\n            malformed = True\n            bad(line_number, str(exc))",
        "after": "        except MalformedEvent as exc:\n            malformed = True\n            bad(line_number, str(exc))\n            return 6",
        "witness": "continue-after-malformed",
        "expected_mismatches": ["stdout"],
    },
    {
        "name": "wrong-priority",
        "purpose": "已有明確失敗時，仍讓 malformed 決定 exit 6。保留診斷以單獨展示 exit 錯誤。",
        "origin": "依 R11 自寫；與凍結 malformed-before-remote-error 為同類失效，但此變異只改 return。",
        "before": "        return 3\n    if malformed:",
        "after": "        return 6 if malformed else 3\n    if malformed:",
        "witness": "explicit-failure-priority",
        "expected_mismatches": ["returncode"],
    },
    {
        "name": "omit-malformed-diagnostic",
        "purpose": "保留 malformed 狀態與 exit 6，卻完全沒有 R03 診斷。",
        "origin": "依 R03 自寫的教學錯法；只改已知 fixture 的 bad 函式。",
        "before": '    print(f"[codex malformed event] line {line_number}: {reason}",\n          file=sys.stderr, flush=True)',
        "after": "    return None  # 故意漏掉診斷；僅供教學",
        "witness": "false-text",
        "expected_mismatches": ["stderr"],
    },
    {
        "name": "buffer-until-eof",
        "purpose": "先讀完整個 stdin 才處理；終態三出口相同，EOF 前沒有有效訊息。",
        "origin": "凍結 test_task_evaluator.py 的 whole_input_buffering 變異方式。",
        "before": "for line_number, line in enumerate(sys.stdin, 1):",
        "after": "for line_number, line in enumerate(sys.stdin.read().splitlines(True), 1):",
        "witness": "stream-before-eof",
        "expected_mismatches": [],
    },
)

LEGAL_VARIATION = {
    "name": "legal-reason-wording",
    "purpose": "只改 malformed REASON 的說明文字；R03 允許不同的非空單行原因。",
    "origin": "依 R03 自寫的合法正對照；不是正式模型候選。",
    "before": 'raise MalformedEvent(field + " must be a string or null")',
    "after": 'raise MalformedEvent("invalid optional text: " + field)',
}


def build_fixtures(directory: Path) -> tuple[dict[str, Path], dict]:
    reference = (SOURCE / "tests/fixtures/parser_reference.py").read_text(encoding="utf-8")
    texts = {"reference": reference}
    derivations = {}
    for mutation in (*MUTATIONS, LEGAL_VARIATION):
        before, after = mutation["before"], mutation["after"]
        if reference.count(before) != 1:
            raise RuntimeError(f"變異位置不唯一：{mutation['name']}")
        text = reference.replace(before, after, 1)
        if text == reference:
            raise RuntimeError("變異未改動來源")
        texts[mutation["name"]] = text
        derivations[mutation["name"]] = mutation
    paths, metadata = {}, {}
    for name, source in texts.items():
        ast.parse(source, filename=name + ".py")
        compile(source, name + ".py", "exec")
        path = directory / (name + ".py")
        path.write_text(source, encoding="utf-8")
        paths[name] = path
        role = ("reference" if name == "reference" else
                "legal-variation" if name == LEGAL_VARIATION["name"] else "known-fault")
        metadata[name] = {"sha256": sha256(path.read_bytes()), "syntax_valid": True, "role": role,
                          "derivation": derivations.get(name, "exact pinned reference fixture")}
    return paths, metadata


def run_batch(path: Path, input_text: str, timeout: float = 5.0) -> Observed:
    completed = subprocess.run([sys.executable, "-I", "-B", str(path)],
                               input=input_text.encode("utf-8"), stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, cwd=path.parent, timeout=timeout,
                               check=False)
    observed = Observed(completed.stdout.decode("utf-8"), completed.stderr.decode("utf-8"),
                        completed.returncode)
    if "Traceback (most recent call last)" in observed.stderr or "SyntaxError" in observed.stderr:
        raise RuntimeError(f"fixture 不是因契約行為被辨識：{path.name}: {observed.stderr}")
    return observed


def stream_probe(path: Path, window: float) -> dict:
    prefix = jsonl(message("stream-before-eof"))
    suffix = jsonl(DONE)
    expected = Expected("stream-before-eof\n" + TOKENS, (), 0)
    proc = subprocess.Popen([sys.executable, "-I", "-B", str(path)], stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=path.parent)
    first_line = queue.Queue()
    chunks = {"stdout": [], "stderr": []}

    def collect(stream, channel):
        for line in iter(stream.readline, b""):
            chunks[channel].append(line)
            if channel == "stdout":
                first_line.put(line)

    threads = [threading.Thread(target=collect, args=(getattr(proc, channel), channel), daemon=True)
               for channel in ("stdout", "stderr")]
    for thread in threads:
        thread.start()
    early = b""
    started = time.monotonic()
    try:
        proc.stdin.write(prefix.encode("utf-8"))
        proc.stdin.flush()
        try:
            early = first_line.get(timeout=window)
        except queue.Empty:
            pass
        # 判斷 EOF 前的輸出之後，才送完成事件並關閉 stdin。
        before_eof = early == b"stream-before-eof\n"
        observation_seconds = time.monotonic() - started
        proc.stdin.write(suffix.encode("utf-8"))
        proc.stdin.close()
        proc.wait(timeout=5.0)
    finally:
        if proc.poll() is None:
            proc.kill()
            proc.wait()
        if not proc.stdin.closed:
            proc.stdin.close()
        for thread in threads:
            thread.join(timeout=1.0)
        proc.stdout.close()
        proc.stderr.close()
    if any(thread.is_alive() for thread in threads):
        raise RuntimeError("stream reader 未正常結束")
    observed = Observed(b"".join(chunks["stdout"]).decode("utf-8"),
                        b"".join(chunks["stderr"]).decode("utf-8"), proc.returncode)
    return {"input_prefix": prefix, "input_after_observation": suffix,
            "observation_window_seconds": window,
            "elapsed_to_pre_eof_observation_seconds": round(observation_seconds, 6),
            "observed_before_eof": before_eof, "early_stdout": early.decode("utf-8"),
            "terminal": asdict(observed), "terminal_grade": grade(expected, observed)}


def run_workbench(window: float = 1.0) -> dict:
    source_before = verify_sources()
    checks = []

    def check(name, condition):
        checks.append({"name": name, "passed": bool(condition)})

    with tempfile.TemporaryDirectory(prefix="trusted-parser-teaching-") as tmp:
        paths, fixtures = build_fixtures(Path(tmp))
        batch = {}
        for name, path in paths.items():
            rows = {}
            for case in cases():
                observed = run_batch(path, case.input_text)
                rows[case.name] = {"requirements": case.requirements, "input": case.input_text,
                                   "expected": asdict(case.expected), "actual": asdict(observed),
                                   "grade": grade(case.expected, observed)}
            batch[name] = rows
            check(name + ": happy path 通過", rows["happy"]["grade"]["passed"])
        check("reference 通過全部四個教學批次案例",
              all(row["grade"]["passed"] for row in batch["reference"].values()))
        check("合法 REASON 改寫通過全部四個教學批次案例",
              all(row["grade"]["passed"] for row in batch[LEGAL_VARIATION["name"]].values()))
        check("合法 REASON 改寫確實產生不同診斷，不能只因與 reference 字串不同而拒絕",
              batch[LEGAL_VARIATION["name"]]["false-text"]["actual"]["stderr"]
              != batch["reference"]["false-text"]["actual"]["stderr"])
        for mutation in MUTATIONS:
            if mutation["name"] != "buffer-until-eof":
                result = batch[mutation["name"]][mutation["witness"]]["grade"]
                check(mutation["name"] + ": 指定錯誤出口被辨識",
                      result["mismatches"] == mutation["expected_mismatches"])
        check("buffer-until-eof 通過全部四個批次終態檢查",
              all(row["grade"]["passed"] for row in batch["buffer-until-eof"].values()))

        streaming = {name: stream_probe(paths[name], window)
                     for name in ("reference", "buffer-until-eof")}
        check("reference 在 EOF 前輸出有效訊息", streaming["reference"]["observed_before_eof"])
        check("buffer-until-eof 在觀察窗內沒有 EOF 前輸出",
              not streaming["buffer-until-eof"]["observed_before_eof"])
        check("streaming 兩份 fixture 的終態三出口都正確",
              all(row["terminal_grade"]["passed"] for row in streaming.values()))
        check("streaming 兩份 fixture 的終態完全相同",
              streaming["reference"]["terminal"] == streaming["buffer-until-eof"]["terminal"])

        base = next(case for case in cases() if case.name == "false-text")
        original = run_batch(paths["reference"], base.input_text)
        shifted = run_batch(paths["reference"], "\n\n" + base.input_text)
        shifted_expected = Expected(base.expected.stdout, (3,), base.expected.returncode)
        check("插空行前後都符合各自契約預期值",
              grade(base.expected, original)["passed"] and grade(shifted_expected, shifted)["passed"])
        check("插入兩空行：stdout／exit 不變，stderr 實體行號由 1 變 3",
              original.stdout == shifted.stdout and original.returncode == shifted.returncode
              and shifted.stderr == original.stderr.replace("line 1: ", "line 3: ", 1)
              and original.stderr != shifted.stderr)

        segment = jsonl(message("same"), DONE)
        once = run_batch(paths["reference"], segment)
        twice = run_batch(paths["reference"], segment + segment)
        check("重複事件前後都符合 R13 預期值",
              grade(Expected("same\n" + TOKENS, (), 0), once)["passed"]
              and grade(Expected(("same\n" + TOKENS) * 2, (), 0), twice)["passed"])
        check("重複事件不是冪等：stdout 重複，exit 與 stderr 不變",
              twice.stdout == once.stdout * 2 and twice.stdout != once.stdout
              and (twice.stderr, twice.returncode) == (once.stderr, once.returncode))
        metamorphic = {
            "blank_lines": {"requirements": ["R02", "R03"], "base_input": base.input_text,
                            "transformed_input": "\n\n" + base.input_text,
                            "base": asdict(original), "transformed": asdict(shifted),
                            "invalid_relation": "三個出口完全不變",
                            "valid_relation": "stdout 與 exit 不變；各 malformed 實體行號增加 2"},
            "duplicate_events": {"requirements": ["R05", "R08", "R13"], "base_input": segment,
                                 "transformed_input": segment + segment,
                                 "base": asdict(once), "transformed": asdict(twice),
                                 "invalid_relation": "重複同一事件片段不改變輸出（冪等）",
                                 "valid_relation": "本例的 stdout 片段重複兩次；exit 0 與空 stderr 不變"},
        }

    source_after = verify_sources()
    check("凍結來源 SHA 在執行前後相同", source_before == source_after)
    return {
        "schema_version": 1,
        "scope": "post-study trusted-fixture teaching; not formal N=40 or the 103-check suite",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment": {"python": sys.version, "implementation": platform.python_implementation(),
                        "system": platform.system(), "release": platform.release(),
                        "machine": platform.machine(), "stdlib_only": True,
                        "execution": "isolated Python mode (-I -B), trusted fixtures, no OS sandbox",
                        "security_claim": "none; Python -I is not an OS sandbox"},
        "workbench_sha256": sha256(Path(__file__).read_bytes()),
        "source_sha256_before": source_before, "source_sha256_after": source_after,
        "fixtures": fixtures, "batch": batch, "streaming": streaming, "metamorphic": metamorphic,
        "checks": checks, "passed": all(row["passed"] for row in checks),
        "limits": ["只有已知 reference、六個單點教學錯法與一個合法改寫，無任何新模型生成。",
                   "不估算 mutation score、模型通過率或錯法在正式候選中的頻率。",
                   "streaming 只測第一則有效訊息，觀察窗受本機排程影響。",
                   "三出口分別比對；不觀察 stdout 與 stderr 之間的全域交錯順序。",
                   "未呼叫正式 evaluator、未執行正式候選、未更改 Seatbelt。",
                   "reference 本身為 AI 撰寫的工具 fixture，不是人工 baseline 或完整正確性證明。"],
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, help="另存完整 JSON；不接受任意 candidate")
    parser.add_argument("--stream-window-seconds", type=float, default=1.0)
    args = parser.parse_args(argv)
    if not 0.1 <= args.stream_window_seconds <= 10.0:
        parser.error("stream window 必須在 0.1 到 10 秒之間")
    result = run_workbench(args.stream_window_seconds)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
        print(json.dumps({"passed": result["passed"], "checks": len(result["checks"]),
                          "output": str(args.output)}, ensure_ascii=False))
    else:
        sys.stdout.write(rendered)
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
