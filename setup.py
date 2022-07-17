import os
from setuptools import setup, find_packages

version = {}
with open(os.path.join("sauron", "_version.py")) as version_file:
    exec(version_file.read(), version)

with open('requirements.txt') as fp:
    required = fp.read().splitlines()

with open('requirements-dev.txt') as fp:
    dev_required = fp.read().splitlines()

setup(
    name="sauron",
    version=version["__version__"],
    description="Open Source Software Security Inspector",
    url="http://github.com/amal-thundiyil/sauron",
    author="Amal Thundiyil",
    author_email="amal.s.thundiyil@gmail.com",
    license="MIT License",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=required,
    extras_require={
        'dev': ['check-manifest'],
        'test': ['coverage'],
    },
)
