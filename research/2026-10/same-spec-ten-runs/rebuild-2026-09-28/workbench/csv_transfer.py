"""Fixed CSV teaching fixtures; no model calls or subprocesses."""
import argparse
import csv
import hashlib
import io
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

INPUT = [
    {"name": "王,小明", "date": None, "note": "第一行\n第二行"},
    {"name": "李", "date": "2026-09-28", "note": ""},
    {"name": "李", "date": "2026-09-28", "note": ""},
]
# Independently transcribed from the teaching contract, not from emit().
EXPECTED_HEADER = ["name", "date", "note"]
EXPECTED_RECORDS = [
    ["王,小明", "", "第一行\n第二行"],
    ["李", "2026-09-28", ""],
    ["李", "2026-09-28", ""],
]


def emit(rows, delimiter):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream, lineterminator=delimiter)
    writer.writerow(["name", "date", "note"])
    for row in rows:
        writer.writerow([row["name"], "" if row["date"] is None else row["date"], row["note"]])
    return stream.getvalue().encode("utf-8")


def parse(data):
    return list(csv.reader(io.StringIO(data.decode("utf-8"), newline=""), strict=True))


def parse_only(data):
    try:
        parse(data)
        return True
    except (UnicodeError, csv.Error):
        return False


def contract_accepts(data):
    try:
        rows = parse(data)
        return bool(rows) and rows[0] == EXPECTED_HEADER and rows[1:] == EXPECTED_RECORDS
    except (UnicodeError, csv.Error):
        return False


def fixtures():
    unique = []
    for row in INPUT:
        if row not in unique:
            unique.append(row)
    lf = emit(INPUT, "\n")
    return {
        "valid_crlf": emit(INPUT, "\r\n"), "valid_lf": lf,
        "deduplicated": emit(unique, "\n"),
        "wrong_header": lf.replace(b"name,date,note", b"date,name,note", 1),
        "wrong_order": emit([INPUT[1], INPUT[0], INPUT[2]], "\n"),
        "wrong_value": lf.replace(b"2026-09-28", b"2026-09-29", 1),
    }


def snapshot(data):
    return {"utf8_text": data.decode("utf-8"), "hex": data.hex(),
            "sha256": hashlib.sha256(data).hexdigest(), "byte_length": len(data)}


def results():
    cases = fixtures()
    observations = {}
    for name, data in cases.items():
        rows = parse(data)
        observations[name] = dict(snapshot(data), physical_lines=len(data.splitlines()),
                                 parsed_header=rows[0], parsed_records=rows[1:],
                                 parse_only_accepts=parse_only(data),
                                 exact_crlf_bytes_accepts=data == cases["valid_crlf"],
                                 contract_accepts=contract_accepts(data))
    input_bytes = (json.dumps(INPUT, ensure_ascii=False, separators=(",", ":")) + "\n").encode("utf-8")
    folder = Path(__file__).resolve().parent
    return {"scope": "Fixed synthetic CSV teaching replay; not a model trial or a second formal repo task.",
            "generated_at_utc": datetime.now(timezone.utc).isoformat(), "python": platform.python_version(),
            "source_sha256": {name: hashlib.sha256((folder / name).read_bytes()).hexdigest()
                              for name in ("csv_transfer.py", "test_csv_transfer.py")},
            "input": snapshot(input_bytes), "expected_header": EXPECTED_HEADER,
            "expected_records": EXPECTED_RECORDS, "observations": observations,
            "limits": ["No general date conversion or full CSV-dialect validation.",
                       "These observations are separate from the original 26 workbench checks."]}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    args.output.write_text(json.dumps(results(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
