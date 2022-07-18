from concurrent.futures import process
import os
import tempfile
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

        repo_name = urlparse(self.url).path.split("/")[2]
        repo_dir = os.path.join(f"{self.repo_dir}", repo_name)
        if not os.path.isdir(repo_dir):
            _ = GitRepository.clone(self.url, repo_dir)

        cmd = [
            "docker",
            "run",
            "--rm",
            "-e",
            f"WORKSPACE={repo_dir}",
            "-v",
            f"{repo_dir}:/app",
            "shiftleft/scan",
            "scan",
            "--build",
        ]
        r = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        reports = self.process_reports(repo_dir)
        return reports

    def process_reports(self, repo_dir):
        l = []
        reports_dir = os.path.join(repo_dir, "reports")
        for filename in os.listdir(reports_dir):
            if filename.startswith("."):
                continue
            with open(os.path.join(reports_dir, filename), "r") as f:
                if filename.endswith(".json"):
                    l.append(filename)

        return l

    def parse_json_reports(self):
        pass

    def parse_csv_reports(self):
        pass
