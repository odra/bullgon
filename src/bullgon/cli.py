"""
Bullgon command line interface module.
"""
import click

from . import __version__

@click.group
def cli() -> None:
    """
    Main cli subcommand aggregator.
    """
    pass


@cli.command
def version() -> None:
    """
    Shows program version to the user.
    """
    click.echo(f'v{__version__}')


def run() -> None:
    """
    This is the function that will be called by the user cli.

    Its sole purpose is to be used as the script main entrypoint.
    """
    try:
        cli()
    except errors.BullgonError as e:
        click.echo(str(e)), err=True)
        click.exit(e.code)
