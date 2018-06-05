import click

from pent import _pipenv, checks


@checks.pipfile_required
def where():
    _pipenv.core.do_where(virtualenv=False, bare=False)
    _pipenv.core.do_where(virtualenv=True, bare=False)


@checks.venv_required
def lock(**kwargs):
    _pipenv.core.do_lock(**kwargs)


@checks.venv_required
def sync(**kwargs):
    # HACK: The second argument is not meaningful. It is a Pipenv bug.
    _pipenv.core.do_sync(click.get_current_context(), None, **kwargs)


@checks.venv_required
def run(**kwargs):
    _pipenv.core.do_run(**kwargs)


@checks.venv_required
def check(**kwargs):
    _pipenv.core.do_check(**kwargs)


@checks.venv_required
def graph(**kwargs):
    _pipenv.core.do_graph(**kwargs)


@checks.venv_required
def clean(**kwargs):
    _pipenv.core.do_clean(click.get_current_context(), **kwargs)
