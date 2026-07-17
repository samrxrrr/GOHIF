from gohif import (
    FRAMEWORK_NAME,
    FRAMEWORK_SHORT_NAME,
    __version__,
)


def test_framework_name() -> None:
    assert FRAMEWORK_NAME == "Global One Health Intelligence Framework"


def test_short_name() -> None:
    assert FRAMEWORK_SHORT_NAME == "GOHIF"


def test_version() -> None:
    assert __version__ == "0.1.0"
