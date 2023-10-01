import pytest
from click.testing import CliRunner


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def mockerr():
    def fn(err):
        def _fn(*args, **kwargs):
            raise err

        return _fn

    return fn
