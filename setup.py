# coding: utf-8
import os.path
from setuptools import setup, find_packages


setup(
    name='untercron',
    version='0.0.1',
    author='Vlad Anonimov',
    author_email='ano@nim.ov',
    description='Mediocre python scheduler lib',
    long_description=open(
        os.path.join(os.path.dirname(__file__), 'README.rst')
    ).read(),
    packages=find_packages(exclude=['tests']),
    setup_requires=['pytest-runner'],
    tests_require=['freezegun', 'pytest'],
)
