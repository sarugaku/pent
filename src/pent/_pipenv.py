"""A wrapper to make Pipenv behave well as a library.
"""

import functools
import os

# Hack to work around Pipenv's annoying import-time side effect of changing
# the current working directory to the project root.
cwd = os.getcwd()
import pipenv.core
import pipenv.utils
os.chdir(cwd)


@functools.lru_cache(maxsize=1)
def get_project():
    return pipenv.core.project


class PythonVersionNotFound(ValueError):
    pass


def get_python_version(executable):
    version = pipenv.utils.python_version(str(executable))
    if not version:
        raise PythonVersionNotFound(executable)
    return version
