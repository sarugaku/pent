import click

from pent import _pipenv, checks


@checks.venv_required
def lock(**kwargs):
    _pipenv.core.do_lock(**kwargs)


@checks.venv_required
def sync(**kwargs):
    # HACK: The second argument is not meaningful. It is a Pipenv bug.
    _pipenv.core.do_sync(click.get_current_context(), None, **kwargs)
