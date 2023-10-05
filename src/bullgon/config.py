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

    def __post_init__(self) -> None:
        """
        Post init method to be executed after the a Config 
        object instance has been created.

        It tries to guess the proper base directory:
        * doesn't do anything if `self.basedir` is already set
        * uses "$XDG_CONFIG_HOME/bullgon" as the top priority path
        * Uses "$HOME/.config/bullgon" as fallback
        """
        if self.base_dir:
            return None 

        xdg_config_dir = os.environ.get('XDG_CONFIG_HOME')
        if xdg_config_dir:
            self.base_dir = f'{xdg_config_dir}/bullgon'
            
            return None

        home_dir = os.environ.get('HOME')
        if home_dir:
            has_cfg_dir = os.path.exists(f'{home_dir}/.config')
            home_cfg_dir = f'{home_dir}/.config/bullgon'
            home_dir = f'{home_dir}/.bullgon'
            self.base_dir = home_cfg_dir if has_cfg_dir else home_dir

            return None
        
        self.base_dir = '/etc/bullgon'

    @property
    def devices_dir(self) -> str:
        return f'{self.base_dir}/devices.d'


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
