import json
import time
from typing import Dict


class AuditLogger:
    """
    Records security-relevant events for embedding integrity.
    """

    def __init__(self, log_path: str = "embeddings/audit_log.json"):
        self.log_path = log_path

    def log_integrity_violation(
        self,
        tampered_tokens: Dict[int, bool],
        vocab: Dict[str, int],
        embedding_file: str
    ):
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())

        violated_tokens = [
            token for token, tid in vocab.items()
            if not tampered_tokens[tid]
        ]

        record = {
            "timestamp": timestamp,
            "embedding_file": embedding_file,
            "violated_tokens": violated_tokens
        }

        self._append(record)

    def _append(self, record: Dict):
        try:
            with open(self.log_path, "r") as f:
                data = json.load(f)
        except FileNotFoundError:
            data = []

        data.append(record)

        with open(self.log_path, "w") as f:
            json.dump(data, f, indent=2)
