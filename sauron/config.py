import json
import os
from pathlib import Path

from sauron import ROOT_SAURON_DIRECTORY

def setenv_from_config(key):
    val = get_from_config(key)
    setenv(key.upper(), val)

def setenv(key, value):
    os.environ[key] = value

def get_config_file():
    config_file_name = "sauron.config.json"
    config_file_path = Path(ROOT_SAURON_DIRECTORY) / config_file_name
    if Path.is_file(config_file_path):
        return str(config_file_path)
    config_dir = Path.home() / ".sauron" 
    config_dir.mkdir(parents=True, exist_ok=True)
    with open(str(config_dir / config_file_name), 'a') as f:
        f.write("")
    return str(config_dir)
    

def get_from_config(key):
    path = get_config_file()
    data = Path(path).read_text()
    config_data = json.loads(data)
    return config_data[key]