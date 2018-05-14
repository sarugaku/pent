import pathlib
import subprocess
import sys

import click
import virtualenv

from pent import _pipenv, checks


def _supports_venv(executable):
    version = _pipenv.get_python_version(executable)
    major, minor, _ = version.split('.', 2)
    major = int(major)
    minor = int(minor)
    if major > 3 or major == 3 and minor >= 4:
        return True
    return False


POSSIBLE_ENV_PYTHON = [
    pathlib.Path('bin', 'python'),
    pathlib.Path('Scripts', 'python.exe'),
]


def _fix_activate_this(venv):
    """Pipenv relies on activate_this.py, but venv does not have this file.

    Fortunately virtualenv's version "just works", so let's grab it.
    """
    for path in POSSIBLE_ENV_PYTHON:
        full_path = venv.joinpath(path)
        if full_path.is_file():
            activate_this = full_path.with_name('activate_this.py')
            click.echo(f'Writing {activate_this}')
            activate_this.write_text(virtualenv.ACTIVATE_THIS)


def _find_venv_python(venv):
    for path in POSSIBLE_ENV_PYTHON:
        full_path = venv.joinpath(path)
        if full_path.is_file():
            return full_path
    raise ValueError(f'no python found in environment')


@checks.pipfile_required
def init(python, prompt, clear):
    project_root = pathlib.Path(_pipenv.get_project().project_directory)
    venv_path = project_root.joinpath('.venv')
    args = [str(venv_path)]

    if venv_path.exists():
        if not clear:
            click.echo(f'Environment exists at {venv_path}', err=True)
            return
        args.append('--clear')

    if not prompt:
        prompt = project_root.name
    args.extend(['--prompt', prompt])

    uses_venv = _supports_venv(python)
    backend = 'venv' if uses_venv else 'virtualenv'
    click.echo(f'Creating new {backend} at {venv_path}', err=True)
    click.echo(f'Using {python}', err=True)

    if uses_venv:
        subprocess.check_call([python, '-m', 'venv'] + args)
        _fix_activate_this(venv_path)
    else:
        subprocess.check_call([
            sys.executable, '-m', 'virtualenv',
            '--quiet', '--python', python,
        ] + args)

    click.echo(f'Making sure pip and Setuptools are up-to-date', err=True)
    subprocess.check_call([
        str(_find_venv_python(venv_path)), '-m', 'pip', 'install',
        '--upgrade', '--disable-pip-version-check', '--quiet',
        'setuptools', 'pip',
    ])
