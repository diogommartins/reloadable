# coding=utf-8
from os import path
from setuptools import setup, find_packages


VERSION = '0.1.5'

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.rst')) as file:
    long_description = file.read()

setup(
    name='reloadable',
    version=VERSION,
    description='Rerun a function upon failure',
    long_description=long_description,
    author='Diogo Magalhães Martins',
    author_email='magalhaesmartins@icloud.com',
    maintainer='www.sieve.com.br',
    maintainer_email='ti@sieve.com.br',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Topic :: Utilities',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6'
    ],
    url='https://bitbucket.org/sievetech/reloadable',
    keywords='reloadable recover decorator loop cli sieve',
    packages=find_packages(exclude=['tests']),
)
