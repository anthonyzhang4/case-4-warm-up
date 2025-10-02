import json
import hashlib
from pathlib import Path
from typing import Mapping, Any
from datetime import datetime

RESULTS_PATH = Path("data/survey.ndjson")

def sha256(value: str) -> str:
    """Return hex digest of a string’s SHA256."""
    if not isinstance(value, str):
        value = str(value)
    return hashlib.sha256(value.encode("utf-8")).hexdigest()

def append_json_line(record: Mapping[str, Any]) -> None:
    """Append one record as a JSON line into results.jsonl."""
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    rec = dict(record)  # copy, don’t mutate input

    # Normalize to strings before hashing
    if "email" in rec and rec["email"]:
        rec["email"] = sha256(str(rec["email"]))
    if "age" in rec and rec["age"] is not None:
        rec["age"] = sha256(str(rec["age"]))

    with RESULTS_PATH.open("a", encoding="utf-8") as f:
        f.write(
            json.dumps(
                rec,
                ensure_ascii=False,
                default=lambda o: o.isoformat() if isinstance(o, datetime) else str(o)
            )
            + "\n"
        )

