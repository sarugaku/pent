import pathlib

from setuptools import find_packages, setup


# Put everything in setup.cfg, except those that don't actually work?
setup(
    package_dir={'': 'src'},
    packages=find_packages('src'),
    version=(
        pathlib.Path(__file__)
        .parent.joinpath('src', 'pent', 'version.txt')
        .read_text().strip()
    ),
)
