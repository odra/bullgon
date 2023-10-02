"""
Bullgon command line interface module.
"""
import sys
from typing import Optional

import click

from . import config, device, errors, __version__

@click.group
@click.option('--base-dir', 
              default=None,
              type=click.Path(exists=True),
              help='optional custom base directory path'
            )
@click.pass_context
def cli(ctx: click.Context, base_dir: Optional[str]) -> None:
    """
    Main cli subcommand aggregator.
    """
    ctx.ensure_object(dict)
    ctx.obj['base_dir'] = base_dir


@cli.command
def version() -> None:
    """
    Shows program version to the user.
    """
    click.echo(f'v{__version__}')


@cli.command
@click.pass_context
def setup(ctx: click.Context) -> None:
    """
    Setups bullgon's base directory for usage.
    """

    cfg = config.Config(ctx.obj['base_dir'])
    
    config.init(cfg)

    click.echo(f'==> INFO: Bullgon initialized at {cfg.base_dir}')


@cli.command
@click.pass_context
@click.argument('device-name', type=str)
def wake(ctx: click.Context, device_name: str) -> None:
    """
    Turns a device on using "wake on lan".

    Device defintions should be stored in "$BASEDIR/devices.d/$DEVICE_NAME.toml".
    """
    cfg = config.Config(ctx.obj['base_dir'])
    dev = config.load_device(cfg, device_name)

    click.echo(f'==> INFO: Trying to wake device "{device_name}..."')
    device.wake(dev)
    click.echo(f'==> INFO: Done.')


def run() -> None:
    """
    This is the function that will be called by the user cli.

    Its sole purpose is to be used as the script's main entrypoint.
    """
    try:
        cli()
    except errors.BullgonError as e:
        click.echo(f'==> ERR: {e.message}', err=True)
        sys.exit(e.code)
