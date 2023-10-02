import pytest

from bullgon import device, errors


def test_device_simple_ok():
    o = device.Device('mydev', 'ZZ:ZZ:ZZ:ZZ:ZZ')

    assert o.name == 'mydev'
    assert o.netmask == '255.255.255.255'
    assert o.port == 9
    assert o.interface is None


def test_device_full_ok():
    o = device.Device('mydev', 'ZZ:ZZ:ZZ:ZZ:ZZ', '255.255.255.50', 14, 'eth5')

    assert o.name == 'mydev'
    assert o.netmask == '255.255.255.50'
    assert o.port == 14
    assert o.interface == 'eth5'


def test_device_err():
    with pytest.raises(errors.BullgonError):
        device.Device('mydev', 'ZZ:ZZ:ZZ:ZZ:ZZ', '255.255.')


def test_device_minimal_from_dict_ok():
    data = {
        'name': 'mydev',
        'mac': 'ZZ:ZZ:ZZ:ZZ:ZZ'
    }

    o = device.from_dict(data)

    assert o.name == 'mydev'
    assert o.mac == 'ZZ:ZZ:ZZ:ZZ:ZZ'
    assert o.netmask == '255.255.255.255'
    assert o.port == 9
    assert o.interface is None


def test_device_full_from_dict_ok():
    data = {
        'name': 'mydev',
        'mac': 'ZZ:ZZ:ZZ:ZZ:ZZ',
        'netmask': '255.255.255.240',
        'port': 50,
        'interface': 'eth10'
    }

    o = device.from_dict(data)

    assert o.name == 'mydev'
    assert o.mac == 'ZZ:ZZ:ZZ:ZZ:ZZ'
    assert o.netmask == '255.255.255.240'
    assert o.port == 50
    assert o.interface == 'eth10'


def test_device_from_dict_error():
    data = {}

    with pytest.raises(errors.BullgonError):
        device.from_dict(data)
