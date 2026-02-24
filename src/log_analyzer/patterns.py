import re

DEFAULT_PATTERNS = {
    "ERROR": re.compile(r"\b(error|failed|failure|critical|panic)\b", re.IGNORECASE),
    "WARNING": re.compile(r"\b(warn|warning|deprecated|retry)\b", re.IGNORECASE),
    "AUTH_FAIL": re.compile(r"\b(failed password|authentication failure|invalid user)\b", re.IGNORECASE),
}
