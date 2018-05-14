import pathlib

import click

from ._click import AliasedGroup, ExecutablePath


@click.group(cls=AliasedGroup)
def cli():
    pass


@cli.command(short_help="Creates a Pipfile in the current working directory.")
def new():
    pipfile_path = pathlib.Path.cwd().joinpath('Pipfile').resolve()
    if pipfile_path.exists():
        click.echo(f'Pipfile exists at {pipfile_path}', err=True)
        return
    click.echo(f'Creating new Pipfile at {pipfile_path}', err=True)
    pipfile_path.touch(exist_ok=False)


@cli.command(short_help="Initializes a virtual environment for this project.")
@click.option(
    '--python', required=True,
    type=ExecutablePath(resolve_path=True),
)
@click.option('--clear', is_flag=True, default=False)
@click.option('--prompt', default=None)
def init(**kwargs):
    from .operations.init import init
    init(**kwargs)


@cli.command(short_help="Resolves dependencies from Pipfile into Pipfile.lock")
@click.option('--clear', is_flag=True, default=False)
@click.option('--pre', is_flag=True, default=False)
@click.option('--keep-outdated', is_flag=True, default=False)
def lock(**kwargs):
    from .operations.misc import lock
    lock(**kwargs)


@cli.command(
    short_help="Installs provided packages and adds them to Pipfile.",
    context_settings={
        'ignore_unknown_options': True,
        'allow_extra_args': True,
    },
)
def install(**kwargs):
    raise NotImplementedError('TODO')


@cli.command(
    short_help="Uninstalls provided packages and removes them from Pipfile.",
)
def uninstall(**kwargs):
    raise NotImplementedError('TODO')


@cli.command(
    short_help="Spawns a shell within the virtual environment.",
    context_settings={
        'ignore_unknown_options': True,
        'allow_extra_args': True,
    },
)
@click.option('--anyway', is_flag=True, default=False)
@click.argument('shell_args', nargs=-1)
def shell(**kwargs):
    raise NotImplementedError('TODO')


@cli.command(short_help="Outputs project and environment information.")
def where():
    from .operations.misc import where
    where()


@cli.command(short_help="Installs all packages specified in Pipfile.lock.")
@click.option('--dev', is_flag=True, default=False)
@click.option('--clear', is_flag=True, default=False)
@click.option('--sequential', is_flag=True, default=False)
def sync(**kwargs):
    from .operations.misc import sync
    sync(**kwargs)


@cli.command(short_help="Uninstalls packages not specified in Pipfile.lock.")
@click.option('--dry-run', is_flag=True, default=False)
def clean(**kwargs):
    from .operations.misc import clean
    clean(**kwargs)


@cli.command(
    short_help="Spawns a command installed into the virtualenv.",
    add_help_option=False,
    context_settings={
        'ignore_unknown_options': True,
        'allow_interspersed_args': False,
        'allow_extra_args': True,
    },
)
@click.argument('command')
@click.argument('args', nargs=-1)
def run(**kwargs):
    from .operations.misc import run
    run(**kwargs)


@cli.command(
    short_help=(
        "Checks for security vulnerabilities and against PEP 508 markers "
        "provided in Pipfile."
    ),
    context_settings={
        'ignore_unknown_options': True,
        'allow_extra_args': True,
    },
)
@click.option('--unused', nargs=1, default=False)
@click.argument('args', nargs=-1)
def check(**kwargs):
    from .operations.misc import check
    check(**kwargs)


@cli.command(
    short_help="Displays currently–installed dependency graph information.",
)
@click.option('--bare', is_flag=True, default=False, help="Minimal output.")
@click.option('--json', is_flag=True, default=False, help="Output JSON.")
@click.option(
    '--reverse', is_flag=True, default=False, help="Reversed dependency graph."
)
def graph(**kwargs):
    from .operations.misc import graph
    graph(**kwargs)


if __name__ == '__main__':
    cli()
