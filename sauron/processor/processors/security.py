import os
import secrets
import tempfile
import json
from pathlib import Path
import subprocess
import shutil
from urllib.parse import urlparse

from git import Repo


class SecurityProcessor:
    def __init__(self, owner, repo) -> None:
        self.url = f"https://github.com/{owner}/{repo}"
        self.name = f"{owner}/{repo}"
        temp_dir = tempfile.gettempdir()  # why does it work only to with /tmp?
        self.repo_path = os.path.join(f"{temp_dir}", f"{owner}_{repo}_{secrets.token_hex(8)}")
        self.reports_dir = Path(self.repo_path) / "reports"

    @classmethod
    def from_url(cls, url, token=None):
        if url.endswith("/"):
            url = url[:-1]
        repo_url = urlparse(url).path[1:]
        owner, repo = repo_url.split("/")
        return cls(owner, repo)

    def process(self):
        self.tools = []
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
                    self.tools.append(tool)
        return self.tools

    def summarize(self, data):
        return data

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
