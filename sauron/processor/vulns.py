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
        self.url = url
        self.repo_dir = tempfile.gettempdir()  # why does it work only to with /tmp?

    def discover_repo(self, url):
        for dir in next(os.walk(self.repo_dir))[1]:
            if url == dir:
                return dir

    def process(self):
        import pdb

        pdb.set_trace()
        repo_name = urlparse(self.url).path.split("/")[2]
        repo_dir = os.path.join(f"{self.repo_dir}", repo_name)
        if not os.path.isdir(repo_dir):
            _ = GitRepository.clone(self.url, repo_dir)

        self.reports_dir = Path.home() / os.path.join(
            ".sauron", "reports", f"{repo_name}_{secrets.token_hex(16)}"
        )
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        cmd = [
            "docker",
            "run",
            "--rm",
            "-e",
            f"WORKSPACE={repo_dir}",
            "-v",
            f"{repo_dir}:/app:cached",
            "quay.io/appthreat/sast-scan",
            "scan",
            "--src",
            "/app",
        ]
        r = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        reports = self.process_reports()
        return reports

    def process_reports(self):
        l = []
        for filename in os.listdir(self.reports_dir):
            if filename.startswith("."):
                continue
            with open(os.path.join(self.reports_dir, filename), "r") as f:
                if filename.endswith(".json"):
                    l.append(filename)

        return l

    def parse_json_reports(self):
        pass

    def parse_csv_reports(self):
        pass
