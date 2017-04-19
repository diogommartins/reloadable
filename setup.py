from setuptools import setup, find_packages
from reloadable import __version__


setup(
    name='reloadable',
    version=__version__,
    description='Rerun a function upon failure',
    url='https://bitbucket.org/sievetech/reloadable',
    packages=find_packages(exclude=['tests']),
)
