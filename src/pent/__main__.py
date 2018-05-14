import pathlib

import click

from ._click import ExecutablePath


@click.group()
def cli():
    pass


@cli.command(short_help="Create a Pipfile in the current working directory.")
def new():
    pipfile_path = pathlib.Path.cwd().joinpath('Pipfile').resolve()
    if pipfile_path.exists():
        click.echo(f'Pipfile exists at {pipfile_path}', err=True)
        return
    click.echo(f'Creating new Pipfile at {pipfile_path}', err=True)
    pipfile_path.touch(exist_ok=False)


@cli.command(short_help="Initialize a virtual environment for this project.")
@click.option(
    '--python', required=True,
    type=ExecutablePath(resolve_path=True),
)
@click.option('--clear', is_flag=True, default=False)
@click.option('--prompt', default=None)
def init(**kwargs):
    from .operations.init import init
    init(**kwargs)


@cli.command(short_help="Installs all packages specified in Pipfile.lock.")
@click.option('--dev', is_flag=True, default=False)
@click.option('--clear', is_flag=True, default=False)
@click.option('--sequential', is_flag=True, default=False)
def sync(**kwargs):
    from . import _pipenv
    # HACK: The second argument is not meaningful. It is a Pipenv bug.
    _pipenv.core.do_sync(click.get_current_context(), None, **kwargs)


if __name__ == '__main__':
    cli()
