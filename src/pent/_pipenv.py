"""A wrapper to make Pipenv behave well as a library.
"""

import functools
import os

# Hack to work around Pipenv's annoying import-time side effect of changing
# the current working directory to the project root.
cwd = os.getcwd()
from pipenv import core, utils
os.chdir(cwd)


@functools.lru_cache(maxsize=1)
def get_project():
    return core.project


class PythonVersionNotFound(ValueError):
    pass


def get_python_version(executable):
    version = utils.python_version(str(executable))
    if not version:
        raise PythonVersionNotFound(executable)
    return version
