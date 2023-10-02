from bullgon import errors
from bullgon.cli import cli, device


def test_cli_wake_ok(runner, monkeypatch):
    dev = device.Device('mock', 'ZZ:ZZ:ZZ:ZZ:ZZ')

    with monkeypatch.context() as m:
        m.setattr('bullgon.config.load_device', lambda d, n: dev)
        m.setattr('bullgon.device.wake', lambda d: None)
        result = runner.invoke(cli, ['wake', 'mock'])

    expected_output = '\n'.join([
        '==> INFO: Trying to wake device "mock..."',
        '==> INFO: Done.',
        ''
    ])
    assert result.exit_code == 0
    assert result.output == expected_output


def test_cli_wake_err(runner, mockerr, monkeypatch):
    err = errors.BullgonError('mock')

    with monkeypatch.context() as m:
        m.setattr('bullgon.config.load_device', mockerr(err))
        result = runner.invoke(cli, ['wake', 'mock'])

    assert result.exit_code == err.code
    assert result.exception == err
