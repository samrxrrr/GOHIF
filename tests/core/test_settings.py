from gae.config.settings import settings


def test_settings_loaded():

    assert settings.timeout > 0

    assert settings.chunk_size > 0

    assert settings.workers > 0
