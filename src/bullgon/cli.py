"""
Bullgon command line interface module.
"""
import sys
from typing import Optional

import click

from . import config, errors, __version__

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

    click.echo(f'==> Bullgon initialized at {cfg.base_dir}')


def run() -> None:
    """
    This is the function that will be called by the user cli.

    Its sole purpose is to be used as the script's main entrypoint.
    """
    try:
        cli()
    except errors.BullgonError as e:
        click.echo(str(e), err=True)
        sys.exit(e.code)
