import pytest

from bullgon import device, errors


def test_device_simple_ok():
    o = device.Device('mydev')

    assert o.name == 'mydev'
    assert o.netmask == '255.255.255.255'
    assert o.port == 9
    assert o.interface is None


def test_device_full_ok():
    o = device.Device('mydev', '255.255.255.50', 14, 'eth5')

    assert o.name == 'mydev'
    assert o.netmask == '255.255.255.50'
    assert o.port == 14
    assert o.interface == 'eth5'


def test_device_err():
    with pytest.raises(errors.BullgonError):
        device.Device('mydev', '255.255.')
