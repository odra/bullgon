import os
import tomllib
from typing import Optional
from dataclasses import dataclass, field

from . import errors, device

@dataclass
class Config:
    """
    Config data class.
    """
    base_dir: Optional[str] = field(default=None)
    devices_dir: str = field(init=False) 

    def __post_init__(self) -> None:
        """
        Post init method to be executed after the a Config 
        object instance has been created.

        It tries to guess the proper base directory:
        * doesn't do anything if `self.basedir` is already set
        * uses "$XDG_CONFIG_HOME/bullgon" as the top priority path
        * Uses "$HOME/.config/bullgon" as fallback
        """
        # TODO: refactor this if-else abomination
        base_dir = self.base_dir

        if base_dir is None:
            xdg_config_dir = os.environ.get('XDG_CONFIG_HOME')
            if xdg_config_dir:
                base_dir = f'{xdg_config_dir}/bullgon'

            home_dir = os.environ.get('HOME')
            if home_dir and base_dir is None:
                if os.path.exists(f'{home_dir}/.config'):
                    base_dir = f'{home_dir}/.config/bullgon'
                else:
                    base_dir = f'{home_dir}/.bullgon'

        self.base_dir = base_dir
        self.devices_dir = f'{self.base_dir}/devices.d'


def init(cfg: Config) -> None:
    """
    Intializes a bullgon config directory.
    """
    try:
        os.makedirs(cfg.devices_dir, exist_ok=True)
    except OSError as e:
        raise errors.BullgonError(e.strerror, e.errno)


def load_device(cfg: Config, name: str) -> device.Device:
    """
    Loads a device from a TOML configuration file
    and return a `bullgon.device.Device` object.
    """
    path = f'{cfg.devices_dir}/{name}.toml'
    if not os.path.exists(path):
        raise errors.BullgonError(f'Could not find {path}')
    
    with open(path, 'rb') as f:
        try:
            data = tomllib.load(f)
        except tomllib.TOMLDecodeError:
            raise errors.BullgonError(f'Failed to parse {path}')

    dev = data.get('device')
    if dev is None:
        raise errors.BullgonError(f'Could not find a "[device]" section in {path}')

    dev['name'] = name

    return device.Device(**data['device'])
