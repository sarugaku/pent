import collections
import contextlib
import importlib
import os
import pathlib
import subprocess
import tempfile

import click

from pent import _pipenv, checks, envs


def _handover(cmd, args):
    args = [cmd] + args
    if os.name != 'nt':
        os.execvp(cmd, args)
    else:
        proc = subprocess.run(args, shell=True, universal_newlines=True)
        click.get_current_context().exit(proc.returncode)


class Shell:

    def __init__(self, cmd):
        self.cmd = cmd
        self.args = []

    @contextlib.contextmanager
    def inject_path(self, venv):
        yield

    def fork(self, venv, cwd):
        click.echo("Launching subshell in virtual environment…", err=True)
        os.environ['VIRTUAL_ENV'] = str(venv)
        with self.inject_path(venv):
            os.chdir(cwd)
            _handover(self.cmd, self.args)


class Bash(Shell):
    # The usual PATH injection technique does not work with Bash.
    # https://github.com/berdario/pew/issues/58#issuecomment-102182346
    @contextlib.contextmanager
    def inject_path(self, venv):
        bashrc_path = pathlib.Path.home().joinpath('.bashrc')
        with tempfile.NamedTemporaryFile('w+') as rcfile:
            if bashrc_path.is_file():
                base_rc_src = 'source "{0}"\n'.format(bashrc_path.as_posix())
                rcfile.write(base_rc_src)

            export_path = 'export PATH="{0}:$PATH"\n'.format(':'.join(
                python.parent.as_posix()
                for python in envs.iter_python(venv)
            ))
            rcfile.write(export_path)
            rcfile.flush()
            self.args.extend(['--rcfile', rcfile.name])
            yield


class CmderEmulatedShell(Shell):
    def fork(self, venv, cwd):
        if cwd:
            os.environ['CMDER_START'] = cwd
        super().fork(venv, cwd)


class CmderCommandPrompt(CmderEmulatedShell):
    def fork(self, venv, cwd):
        rc = os.path.expandvars('%CMDER_ROOT%\\vendor\\init.bat')
        if os.path.exists(rc):
            self.args.extend(['/k', rc])
        super().fork(venv, cwd)


class CmderPowershell(Shell):
    def fork(self, venv, cwd):
        rc = os.path.expandvars('%CMDER_ROOT%\\vendor\\profile.ps1')
        if os.path.exists(rc):
            self.args.extend([
                '-ExecutionPolicy', 'Bypass', '-NoLogo', '-NoProfile',
                '-NoExit', '-Command',
                "Invoke-Expression '. ''{0}'''".format(rc),
            ])
        super().fork(venv, cwd)


# Two dimensional dict. First is the shell type, second is the emulator type.
# Example: SHELL_LOOKUP['powershell']['cmder'] => CmderPowershell.
SHELL_LOOKUP = collections.defaultdict(
    lambda: collections.defaultdict(lambda: Shell),
    {
        'bash': collections.defaultdict(lambda: Bash),
        'cmd': collections.defaultdict(lambda: Shell, {
            'cmder': CmderCommandPrompt,
        }),
        'powershell': collections.defaultdict(lambda: Shell, {
            'cmder': CmderPowershell,
        }),
        'pwsh': collections.defaultdict(lambda: Shell, {
            'cmder': CmderPowershell,
        }),
    },
)


def _get_current_shell(pid=None, max_depth=6):
    try:
        impl = importlib.import_module(f'.{os.name}', 'pent.procdet')
    except ImportError:
        raise RuntimeError(f'shell detection not implemented for {os.name!r}')
    try:
        get_shell = impl.get_shell
    except AttributeError:
        raise RuntimeError(f'get_shell not implemented for {os.name!r}')
    shell = get_shell(pid, max_depth=max_depth)
    if shell:
        return shell
    click.echo(
        'Cannot detect your shell. Set the PIPENV_SHELL environment '
        'variable explicitly to tell Pent what to use.',
        err=True,
    )
    click.get_current_context().exit(1)


def _get_current_emulator():
    if os.environ.get('CMDER_ROOT'):
        return 'cmder'
    return ''


def _choose_shell():
    try:
        shell_cmd = os.environ['PIPENV_SHELL']
    except KeyError:
        shell_cmd = _get_current_shell()
    try:
        emulator = os.environ['PIPENV_EMULATOR']
    except KeyError:
        emulator = _get_current_emulator()
    shell_cls = SHELL_LOOKUP[pathlib.Path(shell_cmd).stem.lower()][emulator]
    return shell_cls(shell_cmd)


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
    shell = _choose_shell()
    shell.args.extend(args)
    shell.fork(_pipenv.get_venv_path(), os.getcwd())
