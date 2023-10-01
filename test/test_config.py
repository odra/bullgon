import os

import pytest

from bullgon import config, errors


def test_config_custom_ok():
    cfg = config.Config(base_dir='/tmp/bullgon')

    assert cfg.base_dir == '/tmp/bullgon'
    assert cfg.devices_dir == '/tmp/bullgon/devices.d'


@pytest.mark.parametrize('env_name,env_value,base_dir,mock_dir', [
    ('XDG_CONFIG_HOME', '/home/user/.config', '/home/user/.config/bullgon',
     False),
    ('HOME', '/home/user2', '/home/user2/.config/bullgon', True),
    ('HOME', '/root', '/root/.bullgon', False)
])
def test_config_env_ok(monkeypatch, env_name, env_value, base_dir, mock_dir):
    with monkeypatch.context() as m:
        m.setenv(env_name, env_value)
        if mock_dir:
            m.setattr('os.path.exists', lambda path: True)
        cfg = config.Config()

    assert cfg.base_dir == base_dir
    assert cfg.devices_dir == f'{base_dir}/devices.d'


def test_config_init_ok(tmp_path):
    path = f'{tmp_path}/config/bullgon'
    cfg = config.Config(path)

    config.init(cfg)

    assert os.path.exists(path)


def test_config_init_error(monkeypatch, mockerr):
    with monkeypatch.context() as m:
        m.setattr('os.makedirs', mockerr(OSError(1, 'os.error.mock')))
        with pytest.raises(errors.BullgonError):
            config.init(config.Config())
