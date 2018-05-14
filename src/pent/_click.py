import os
import pathlib

import click


class ExecutablePath(click.Path):
    """A path that also checks PATH for executables.
    """
    def __init__(self, **kwargs):
        super().__init__(exists=True, dir_okay=False, file_okay=True, **kwargs)

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


class AliasedGroup(click.Group):

    aliases = {
        'add': 'install',
        'remove': 'uninstall',
    }

    def get_command(self, ctx, cmd_name):
        cmd_name = self.aliases.get(cmd_name, cmd_name)
        return super().get_command(ctx, cmd_name)
