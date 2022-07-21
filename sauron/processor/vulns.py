from concurrent.futures import process
import os
import tempfile
import secrets
import json
from pathlib import Path
import subprocess
from urllib.parse import urlparse
from isort import file
from git import Repo


from perceval.backends.core.git import GitRepository

from sauron import ROOT_SAURON_DIRECTORY


class VulnsProcessor:
    def __init__(self, url) -> None:
        self.url = url
        self.temp_dir = tempfile.gettempdir()  # why does it work only to with /tmp?
        self.repo_url = urlparse(url).path[1:]
        self.repo_name = "_".join(self.repo_url.split("/"))
        self.repo_path = os.path.join(f"{self.temp_dir}", self.repo_name)
        self.reports_dir = Path(self.repo_path) / "reports"

    def process(self):
        tools = []
        _ = self.run_sast_scan()
        for file in os.listdir(self.reports_dir):
            if not file.startswith("all"):
                continue
            with open(os.path.join(self.reports_dir, file), "r") as fp:
                json_data = fp.read()
                for line in json_data.split("\n"):
                    if not line.strip():
                        continue
                    try:
                        sarif_data = json.loads(line)
                    except Exception:
                        continue
                    try:
                        tool = {
                            "name": sarif_data["tool"]["driver"]["name"],
                            "low": sarif_data["properties"]["metrics"]["low"],
                            "medium": sarif_data["properties"]["metrics"]["medium"],
                            "high": sarif_data["properties"]["metrics"]["high"],
                            "critical": sarif_data["properties"]["metrics"]["critical"],
                            "total": sarif_data["properties"]["metrics"]["total"],
                            "status": sarif_data["invocations"][0][
                                "executionSuccessful"
                            ],
                        }
                    except:
                        continue
                    tools.append(tool)

        return tools

    def run_sast_scan(self):
        if not os.path.isdir(self.repo_path):
            g = Repo.clone_from(self.url, self.repo_path)
        cmd = [
            "docker",
            "run",
            "--rm",
            "-e",
            f"WORKSPACE={self.repo_path}",
            "-v",
            f"{self.repo_path}:/app:cached",
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
        return r
