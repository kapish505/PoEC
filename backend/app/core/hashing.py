import hashlib
import json
from typing import Any

def canonical_json(data: Any) -> bytes:
    """
    Produce a canonical JSON representation of data (sorted keys, no whitespace).
    """
    return json.dumps(data, sort_keys=True, separators=(',', ':'), default=str).encode('utf-8')

def hash_content(data: Any) -> str:
    """
    Compute SHA-256 hash of the canonical JSON representation of data.
    """
    raw_bytes = canonical_json(data)
    return hashlib.sha256(raw_bytes).hexdigest()
