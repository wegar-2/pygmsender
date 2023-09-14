from setuptools import setup, find_packages


def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()


def read_file(file):
    with open(file) as f:
        return f.read()


short_description = "Package for simple dispatch of emails in Python from your gmail account"
long_description = """
Package handles the tasks related to the simple dispatch of emails in Python from your gmail account.
"""

setup(
    name='pygmsender',
    version="0.0.1",
    author='Artur Wegrzyn',
    author_email='awegrzyn17@gmail.com',
    description='',
    long_description=long_description,
    packages=find_packages(exclude=["test"]),  # Don't include test directory in binary distribution
)
