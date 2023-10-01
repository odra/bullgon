from bullgon import errors
from bullgon.cli import cli


def test_cli_setup_ok(runner, tmp_path):
    result = runner.invoke(cli, ['--base-dir', tmp_path, 'setup'])

    assert result.exit_code == 0
    assert result.output == f'==> Bullgon initialized at {tmp_path}\n'


def test_cli_setup_err(runner, mockerr, monkeypatch):
    err = errors.BullgonError('mock')

    with monkeypatch.context() as m:
        m.setattr('bullgon.config.init', mockerr(err))
        result = runner.invoke(cli, ['setup'])

    assert result.exit_code == err.code
    assert result.exception == err
