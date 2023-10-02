from bullgon import __version__
from bullgon.cli import cli


def test_version(runner):
    result = runner.invoke(cli, ['version'])

    assert result.exit_code == 0
    assert result.output == f'v{__version__}\n'
