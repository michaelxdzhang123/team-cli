import re
from typing import Iterable


def redact_secret(value: str, secrets: Iterable[str]) -> str:
    redacted = value
    for secret in {s for s in secrets if s}:
        redacted = re.sub(re.escape(secret), "***", redacted)
    redacted = re.sub(r"(Authorization:\s*)(Bearer|token)\s+[A-Za-z0-9\-\.\_\~\+\/=]+", r"\1***", redacted, flags=re.IGNORECASE)
    redacted = re.sub(r"(token=)[^&\s]+", r"\1***", redacted, flags=re.IGNORECASE)
    return redacted


def redact_headers(headers: dict[str, str]) -> dict[str, str]:
    return {k: redact_secret(v, [v]) for k, v in headers.items()}
