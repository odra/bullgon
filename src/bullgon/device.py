import re
from typing import Optional
from dataclasses import dataclass, field

from . import errors

@dataclass
class Device:
    """
    Device dataclass that represents a device
    for bullgon to interact with.
    """
    name: str
    netmask: str = field(default='255.255.255.255')
    port: int = field(default=9)
    interface: Optional[str] = field(default=None)

    def __post_init__(self) -> None:
        """
        Post intialization dataclass method,
        used for field validation.
        """
        if re.match('\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', self.netmask) is None:
            raise errors.BullgonError('invalid netmask ip: {self.netmask}')
