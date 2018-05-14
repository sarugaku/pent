import functools
import pathlib

import click

from . import _pipenv


def pipfile_required(f):

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not _pipenv.get_project().pipfile_exists:
            click.echo('Pipfile not found! You need to run "pent new" first.')
            click.get_current_context().exit(1)
        return f(*args, **kwargs)

    return wrapped


def venv_required(f):

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        pipfile_location = _pipenv.get_project().pipfile_location
        if not pipfile_location:
            click.echo('Pipfile not found! You need to run "pent new" first.')
            click.get_current_context().exit(1)
        pipfile_path = pathlib.Path(pipfile_location)
        if not pipfile_path.is_file():
            click.echo('Pipfile not found! You need to run "pent new" first.')
            click.get_current_context().exit(1)
        if not pipfile_path.with_name('.venv').is_dir():
            click.echo(
                'Virtual environment not found! '
                'You need to run "pent init" first.',
            )
            click.get_current_context().exit(1)
        return f(*args, **kwargs)

    return wrapped
