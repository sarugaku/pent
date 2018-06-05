import os
import pathlib
import re

import click
import pythonfinder


PYTHON_VERSION_PATTERN = re.compile(r'^(\d+)(?:\.(\d+))?$')


def find_by_version(major, minor):
    finder = pythonfinder.Finder()
    return finder.find_python_version(major, minor)


def find_in_system_path(val):
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
                return full_path.resolve()
    return None


class PythonExecutablePath(click.Path):
    """A path that also checks PATH for Python executables.
    """
    def __init__(self, **kwargs):
        super().__init__(exists=True, dir_okay=False, file_okay=True, **kwargs)

    def convert(self, val, param, ctx):
        match = PYTHON_VERSION_PATTERN.match(val)
        if match:
            # This looks like a Python version. Try to find it.
            entry = find_by_version(*(
                int(c) if c else None
                for c in match.groups()
            ))
            if entry and entry.path:
                val = str(entry.path.resolve())
        if 'PATH' in os.environ and os.path.sep not in val and '/' not in val:
            # This looks like a command. Try to resolve it before checking.
            path = find_in_system_path(val)
            if path:
                val = str(path.resolve())
        return super().convert(val, param, ctx)


class AliasedGroup(click.Group):

    aliases = {
        'add': 'install',
        'remove': 'uninstall',
    }

    def get_command(self, ctx, cmd_name):
        cmd_name = self.aliases.get(cmd_name, cmd_name)
        return super().get_command(ctx, cmd_name)
