import os

import click

from pent import _pipenv, checks


@checks.venv_required
def shell(args, anyway):
    if 'PIPENV_ACTIVE' in os.environ:
        envname = os.environ.get('VIRTUAL_ENV', 'UNKNOWN_VIRTUAL_ENVIRONMENT')
        if not anyway:
            click.echo(
                f'Shell for {envname} is active.\n'
                f'No action taken to avoid nested environments.',
                err=True,
            )
            return
    _pipenv.shells.choose_shell().fork(
        _pipenv.get_venv_path(),
        os.getcwd(),
        args,
    )
