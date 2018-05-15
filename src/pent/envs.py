import pathlib


POSSIBLE_ENV_PYTHON = [
    pathlib.Path('bin', 'python'),
    pathlib.Path('Scripts', 'python.exe'),
]


def iter_python(venv):
    for path in POSSIBLE_ENV_PYTHON:
        full_path = venv.joinpath(path)
        if full_path.is_file():
            yield full_path
