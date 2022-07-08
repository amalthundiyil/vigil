import os
from setuptools import setup, find_packages

version = {}
with open(os.path.join("sauron", "_version.py")) as version_file:
    exec(version_file.read(), version)

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
    install_requires=[],
    extras_require={"dev": ["black"]},
)
