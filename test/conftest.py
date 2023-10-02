import os

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


@pytest.fixture
def test_dir():
    return os.path.dirname(os.path.realpath(__file__))


@pytest.fixture
def fixture_dir(test_dir):
    return f'{test_dir}/fixtures'


@pytest.fixture
def devices_dir(fixture_dir):
    return f'{fixture_dir}/devices.d'
