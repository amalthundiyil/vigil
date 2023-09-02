import os
from setuptools import setup, find_packages

version = {}
with open(os.path.join("vigil", "_version.py")) as version_file:
    exec(version_file.read(), version)

with open("requirements.txt") as fp:
    required = fp.read().splitlines()

with open("requirements-dev.txt") as fp:
    dev_required = fp.read().splitlines()

with open('README.md') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()


setup(
    name="vigil",
    version=version["__version__"],
    description="Open Source Software Security Inspector",
    long_description=readme,
    url="http://github.com/amal-thundiyil/vigil",
    author="Amal Thundiyil",
    author_email="amal.s.thundiyil@gmail.com",
    license=license,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=required,
    extras_require={
        "dev": dev_required,
    },
    entry_points={
        "console_scripts": [
            "vigil = vigil.cli.cli:cli",
        ],
    },
)
