from urllib.parse import urlparse
import json
from datetime import datetime
import subprocess

import requests

from hosts.github import Github
from base.backend import BackendTypes, BaseBackend, BackendUrls
from config import setenv_from_config


class Pypi(BaseBackend):
    def __init__(self, name, token=None) -> None:
        self.name = name
        self.type = BackendTypes.pypi
        self.url = f"https://{BackendUrls.pypi_url}/project/{name}"
        self.token = token
        self.repo = self.get_repo()
        self.host = self.get_repository()
        self.security_metrics = None

    @classmethod
    def from_url(cls, url, token):
        if url.endswith("/"):
            url = url[:-1]
        repo_url = urlparse(url).path[1:]
        owner, repo = repo_url.split("/")
        return cls(repo, token)

    @classmethod
    def from_name(cls, name, token):
        return cls(name, token)

    def get_repo(self):
        setenv_from_config("libraries_api_key")
        from pybraries.search import Search

        self.search = Search()
        info = self.search.project("pypi", self.name)
        return info

    def get_repository(self):
        url = self.repo["repository_url"]
        parsed_url = urlparse(url)
        if "github" in parsed_url.netloc:
            return Github.from_url(url, self.token)

    def downloads_data(self):
        r = requests.get(f"https://api.pepy.tech/api/projects/{self.name}")
        if not r.ok:
            return
        obj = r.json()
        now = datetime.now()
        downloads = []
        for k, v in obj["downloads"].items():
            dt = datetime.strptime(k, "%Y-%m-%d")
            delta = now - dt
            if delta.days <= 7:
                downloads.append({"downloads": int(v), "day": k})
        if not downloads and self.host:
            return self.host.downloads_data()
        return downloads

    def security(self):
        if self.security_metrics is not None:
            return self.security_metrics
        result = subprocess.run(
            f"scorecard --repo={self.url} --format json",
            shell=True,
            env={"GITHUB_AUTH_TOKEN": self.token},
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        if "error" in result.stdout.decode("utf-8") or result.stderr.decode("utf-8"):
            return self.host.security()
        scorecard_output = result.stdout.decode("utf-8")
        scorecard_output = scorecard_output[scorecard_output.find("{") :]
        js = json.loads(scorecard_output)

        self.security_metrics = []
        for check in js.get("checks", []):
            payload = {
                "metric": check["name"].lower().replace("-", "_"),
                "description": check["reason"],
                "score": check["score"],
            }
            self.security_metrics.append(payload)
        return self.security_metrics

    @property
    def forks(self):
        return self.repo["forks"]

    @property
    def contributor_count(self):
        d = self.search.project_contributors("pypi", self.name)
        return len(d)

    @property
    def stars_count(self):
        return self.repo["stars"]

    @property
    def dependents_count(self):
        d = self.search.project_dependent_repositories("pypi", self.name)
        return len(d)
