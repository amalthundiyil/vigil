from concurrent.futures import process
import os
import tempfile
import secrets
from pathlib import Path
import subprocess
from urllib.parse import urlparse
from isort import file

from perceval.backends.core.git import GitRepository

from sauron import ROOT_SAURON_DIRECTORY


class VulnsProcessor:
    def __init__(self, url) -> None:
        self.repo_dir = tempfile.gettempdir()  # why does it work only to with /tmp?
        self.repo_name = urlparse(url).path[1:]
        self.repo_dir = os.path.join(f"{self.repo_dir}", self.repo_name)

    def discover_repo(self, url):
        for dir in next(os.walk(self.repo_dir))[1]:
            if url == dir:
                return dir

    def process(self):
        if not os.path.isdir(self.repo_dir):
            _ = GitRepository.clone(self.url, self.repo_dir)
        cmd = [
            "docker",
            "run",
            "--rm",
            "-e",
            f"WORKSPACE={self.repo_dir}",
            "-v",
            f"{self.repo_dir}:/app:cached",
            "amalthundiyil/sast-scan",
            "scan",
            "--src",
            "/app",
        ]
        r = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return r