"""Report incomplete campaign slots without pretending they are measured failures."""
import argparse
from collections import Counter
import json
from pathlib import Path


def status(campaign):
    manifest = json.loads((campaign / "manifest.json").read_text())
    schedule = manifest["schedule"]
    expected = {item["run_id"] for item in schedule}
    if len(expected) != len(schedule):
        raise ValueError("Duplicate scheduled slot")
    rows = {}
    if (campaign / "records.jsonl").exists():
        for line in (campaign / "records.jsonl").read_text().splitlines():
            row = json.loads(line)
            key = row["run_id"]
            if key not in expected or key in rows:
                raise ValueError("Unknown or duplicate result")
            rows[key] = row
    slots = []
    for item in schedule:
        key = item["run_id"]
        if key in rows:
            state = rows[key]["status"]
        elif (campaign / key / "generation.json").exists():
            state = "generated_not_scored"
        elif (campaign / key).exists():
            state = "started_without_record"
        else:
            state = "not_started"
        slots.append({**item, "status": state, "recorded": key in rows})
    halt_marker = (campaign / "HALTED.json").exists()
    recorded_violation = any(row.get("boundary_violation") is True or row.get("status") == "boundary_failure"
                             for row in rows.values())
    halted = halt_marker or recorded_violation
    return {"complete": len(rows) == len(schedule) and not halted, "halted": halted,
            "halt_marker_present": halt_marker, "boundary_violation_in_ledger": recorded_violation,
            "planned": len(schedule), "recorded": len(rows),
            "counts": dict(Counter(row["status"] for row in slots)), "slots": slots,
            "confidence_intervals": "not computed by status report; complete campaigns use analyze.py"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("campaign", type=Path)
    args = parser.parse_args()
    print(json.dumps(status(args.campaign), indent=2))
