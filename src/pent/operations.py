import functools
import pathlib
import subprocess
import sys

import click

from . import _pipenv


def _pipfile_required(f):

    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        if not _pipenv.get_project().pipfile_exists:
            click.echo('Pipfile not found! You need to run "pent new" first.')
            click.get_current_context().exit(1)
        return f(*args, **kwargs)

    return wrapped


def new():
    pipfile_path = pathlib.Path.cwd().joinpath('Pipfile').resolve()
    if pipfile_path.exists():
        click.echo(f'Pipfile exists at {pipfile_path}', err=True)
        return
    click.echo(f'Creating new Pipfile at {pipfile_path}', err=True)
    pipfile_path.touch(exist_ok=False)


def _supports_venv(executable):
    version = _pipenv.get_python_version(executable)
    major, minor, _ = version.split('.', 2)
    major = int(major)
    minor = int(minor)
    if major > 3 or major == 3 and minor >= 4:
        return


def _find_env_python(venv):
    possibilities = [
        venv.joinpath('bin', 'python'),
        venv.joinpath('Scripts', 'python.exe'),
    ]
    for path in possibilities:
        if path.is_file():
            return path
    raise ValueError(f'no python found in environment')


@_pipfile_required
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

    if _supports_venv(python):
        args = [python, '-m', 'venv'] + args
    else:
        args = [sys.executable, '-m', 'virtualenv', '--quiet'] + args

    click.echo(f'Creating new virtual environment at {venv_path}', err=True)
    click.echo(f'Using {python}', err=True)
    subprocess.check_call(args)

    click.echo(f'Making sure pip and Setuptools are up-to-date', err=True)
    subprocess.check_call([
        str(_find_env_python(venv_path)), '-m', 'pip', 'install',
        '--upgrade', '--disable-pip-version-check', '--quiet',
        'setuptools', 'pip',
    ])
