import os
import pathlib

import click


@click.group()
def cli():
    pass


@cli.command(short_help='Create a Pipfile in the current working directory.')
def new(**kwargs):
    from .operations import new
    new(**kwargs)


class ExecutablePath(click.Path):
    def convert(self, val, param, ctx):
        if 'PATH' in os.environ and os.path.sep not in val and '/' not in val:
            # This looks like a command. Try to resolve it before checking.
            choices = [val]
            if 'PATHEXT' in os.environ:
                choices += [
                    f'{val}{ext}'
                    for ext in os.environ['PATHEXT'].split(os.pathsep)
                ]
            for choice in choices:
                for path in os.environ['PATH'].split(os.pathsep):
                    full_path = pathlib.Path(path, choice)
                    if full_path.is_file():
                        val = str(full_path.resolve())
                        break
        return super().convert(val, param, ctx)


@cli.command(short_help='Initialize a virtual environment for this project.')
@click.option(
    '--python', required=True,
    type=ExecutablePath(exists=True, dir_okay=False, resolve_path=True),
)
@click.option('--clear', default=False)
@click.option('--prompt', default=None)
def init(**kwargs):
    from .operations import init
    init(**kwargs)


if __name__ == '__main__':
    cli()
