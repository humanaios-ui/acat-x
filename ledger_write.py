#!/usr/bin/env python3
"""
Ledger Write — Proofreading Polymerase (E1)

Single append function for all tools to call. Records are chained:
each record includes prev_hash (hash of the previous record).

Chokepoint design: all tools call ledger_write.append() instead of writing directly.
Falsifier: if any tool writes outside this function, the mechanism failed.
"""

import json
import hashlib
import time
from pathlib import Path
from typing import Any, Dict, Optional

LEDGER_PATH = Path(".empirica/event_ledger.jsonl")

def _compute_hash(record: Dict[str, Any]) -> str:
    """SHA256 hash (deterministic JSON)."""
    serialized = json.dumps(record, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(serialized.encode()).hexdigest()

def _read_last_hash() -> Optional[str]:
    """Get hash of last record."""
    if not LEDGER_PATH.exists():
        return None
    try:
        with open(LEDGER_PATH, 'r') as f:
            last_line = None
            for line in f:
                last_line = line.strip()
            if last_line:
                return json.loads(last_line).get('_hash')
    except Exception as e:
        print(f"Warning: {e}")
    return None

def append(record: Dict[str, Any], substrate: str = "acat-x", tool_name: Optional[str] = None) -> str:
    """Append record with chaining. Returns hash of new record."""
    LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    prev_hash = _read_last_hash()
    chained = {**record, "_substrate": substrate, "_tool": tool_name, "_timestamp": time.time(), "_prev_hash": prev_hash}
    record_hash = _compute_hash(chained)
    chained["_hash"] = record_hash
    with open(LEDGER_PATH, 'a') as f:
        f.write(json.dumps(chained, separators=(',', ':')) + '\n')
    return record_hash

def verify_chain() -> bool:
    """Verify chain integrity."""
    if not LEDGER_PATH.exists():
        return True
    try:
        prev_hash = None
        with open(LEDGER_PATH, 'r') as f:
            for line_num, line in enumerate(f, 1):
                record = json.loads(line.strip())
                stored_hash = record.pop("_hash", None)
                if _compute_hash(record) != stored_hash or record.get("_prev_hash") != prev_hash:
                    return False
                prev_hash = stored_hash
        return True
    except:
        return False
