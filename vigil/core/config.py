import json
import os
import logging

from pathlib import Path

from constants import PROJECT_ROOT_DIRECTORY

LOGGER = logging.getLogger()


def setenv_from_config(key):
    val = get_from_config(key)
    setenv(key.upper(), val)


def setenv(key, value):
    os.environ[key] = value


def get_config_file():
    config_file_name = "vigil.config.json"
    config_file_path = Path(PROJECT_ROOT_DIRECTORY) / config_file_name
    # need to pip install -e . for finding the config in project root dir
    if Path.is_file(config_file_path):
        return str(config_file_path)
    config_dir = Path.home() / ".vigil"
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(str(config_dir / config_file_name), "a") as f:
        f.write("")
    return str(config_dir / config_file_name)


def get_from_config(key):
    path = get_config_file()
    data = Path(path).read_text()
    config_data = json.loads(data)
    return config_data[key]
