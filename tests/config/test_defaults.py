from gohif.config.defaults import (
    DEFAULT_PROJECT_NAME,
    DEFAULT_DATABASE,
    DEFAULT_ENVIRONMENT,
)


def test_project_name() -> None:
    assert DEFAULT_PROJECT_NAME == "GOHIF"


def test_database() -> None:
    assert DEFAULT_DATABASE == "duckdb"


def test_environment() -> None:
    assert DEFAULT_ENVIRONMENT == "development"
