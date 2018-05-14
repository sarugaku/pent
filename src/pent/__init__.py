import pathlib


__version__ = (
    pathlib.Path(__file__).with_name('version.txt')
    .read_text().strip()
)
