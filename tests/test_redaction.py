from team_ai.redaction import redact_secret


def test_redact_secret_hides_token() -> None:
    text = "Authorization: Bearer secret-token-123"
    redacted = redact_secret(text, ["secret-token-123"])
    assert "secret-token-123" not in redacted
    assert "***" in redacted


def test_redact_query_token() -> None:
    text = "https://example.com/api?token=abc123&other=1"
    redacted = redact_secret(text, ["abc123"])
    assert "abc123" not in redacted
    assert "token=***" in redacted
