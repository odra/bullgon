import re
import socket
from typing import Any, Dict, Optional
from dataclasses import dataclass, field

from . import errors

@dataclass
class Device:
    """
    Device dataclass that represents a device
    for bullgon to interact with.
    """
    name: str
    mac: str
    netmask: str = field(default='255.255.255.255')
    port: int = field(default=9)
    interface: Optional[str] = field(default=None)

    def __post_init__(self) -> None:
        """
        Post intialization dataclass method,
        used for field validation.
        """
        if re.match(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', self.netmask) is None:
            raise errors.BullgonError('invalid netmask ip: {self.netmask}')


# TODO: replace "Any" with proper typing definition
def from_dict(data: Dict[str, Any]) -> Device:
    """
    Creates a new device object from a dictionary.

    The dicionary will be "forwarded" as `Device(**data)`
    (`data` being said dictionary).
    """
    try:
        return Device(**data)
    except TypeError:
        raise errors.BullgonError('Failed to initialize device')


def wake(dev: Device) -> None:
    mac = dev.mac.replace(':', '')
    packet = bytes.fromhex('F' * 12 + mac * 16)

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        if dev.interface is not None:
            interface = f'{dev.interface}\0'.encode('utf-8')
            s.setsockopt(socket.SOL_SOCKET, 25, interface)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        s.connect((dev.netmask, dev.port))

        s.send(packet)
        s.close()
