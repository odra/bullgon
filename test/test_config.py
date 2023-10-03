import os

import pytest

from bullgon import config, device, errors


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
        monkeypatch.delenv('XDG_CONFIG_HOME', raising=False)
        monkeypatch.delenv('HOME', raising=False)
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


def test_load_device_minimal_ok(fixture_dir):
    cfg = config.Config(fixture_dir)
    expected_obj = device.Device('minimal', 'ZZ::ZZ:ZZ:ZZ:ZZ')
    obj = config.load_device(cfg, 'minimal')

    assert obj == expected_obj


def test_load_device_full_ok(fixture_dir):
    cfg = config.Config(fixture_dir)
    expected_obj = device.Device('full',
                                 'ZZ::ZZ:ZZ:ZZ:ZZ',
                                 '255.255.255.250',
                                 39,
                                 'eth10')
    obj = config.load_device(cfg, 'full')

    assert obj == expected_obj

def test_load_device_path_error(fixture_dir):
    cfg = config.Config(fixture_dir)

    with pytest.raises(errors.BullgonError):
        config.load_device(cfg, '404')


def test_load_device_parse_error(fixture_dir):
    cfg = config.Config(fixture_dir)

    with pytest.raises(errors.BullgonError):
        config.load_device(cfg, 'invalid')


def test_load_device_section_error(fixture_dir):
    cfg = config.Config(fixture_dir)

    with pytest.raises(errors.BullgonError):
        config.load_device(cfg, 'missing')
