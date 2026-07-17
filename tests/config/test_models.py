from gohif.config.models import (
    LoggingConfig,
    ProjectConfig,
    RuntimeConfig,
    StorageConfig,
)


def test_project_model():

    cfg = ProjectConfig(
        name="GOHIF",
        version="0.1.0",
        author="GOHIF Consortium",
    )

    assert cfg.name == "GOHIF"


def test_logging_model():

    cfg = LoggingConfig(
        level="INFO",
        directory="logs",
    )

    assert cfg.level == "INFO"


def test_storage_model():

    cfg = StorageConfig(
        data_directory="data",
        output_directory="results",
        database="duckdb",
        database_file="gohif.duckdb",
    )

    assert cfg.database == "duckdb"


def test_runtime_model():

    cfg = RuntimeConfig(
        environment="development",
        threads=4,
        random_seed=42,
    )

    assert cfg.environment == "development"
