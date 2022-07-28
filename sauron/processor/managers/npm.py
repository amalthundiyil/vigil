from urllib.parse import urlparse
import json
import subprocess

import requests

from sauron.processor.hosts.github import Github
from sauron.processor.base_backend import BackendTypes, BaseBackend, BackendUrls


class Npm(BaseBackend):
    def __init__(self, name, token=None) -> None:
        self.name = name
        self.url = f"https://{BackendUrls.npm_url}/package/{name}"
        self.type = BackendTypes.npm
        self.token = token
        self.repo = self.get_repo()
        self.host = self.get_repository()
        self.result = {}

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
        url = f"https://registry.npmjs.org/{self.name}"
        r = requests.get(url)
        obj = {}
        if r.status_code < 400 and r.status_code >= 200:
            obj = r.json()
        return obj

    def get_repository(self):
        url = self.repo["repository"]["url"]
        parsed_url = urlparse(url)
        if "github" in parsed_url.netloc:
            return Github.from_url(url, self.token)

    def security(self):
        if self.security_metrics is not None:
            return self.security_metrics
        result = subprocess.run(
            f'docker run --rm -it --env "GITHUB_AUTH_TOKEN={self.token}" gcr.io/openssf/scorecard:stable --npm={self.name} --format json',
            shell=True,
            stdout=subprocess.PIPE,
        )
        scorecard_output = result.stdout.decode("utf-8")
        scorecard_output = scorecard_output[scorecard_output.find("{") :]
        js = json.loads(scorecard_output)

        self.security_metrics = []
        for check in js.get("checks", []):
            payload = {
                "metric": check["name"].lower().replace('-', '_'),
                "description": check["reason"],
                "score": check["score"],
            }
            self.security_metrics.append(payload)
        return self.security_metrics

    def downloads_data(self):
        r = requests.get(f"https://api.npmjs.org/downloads/range/last-week/{self.name}")
        if r.status_code < 400 and r.status_code >= 200:
            obj = r.json()
            return obj["downloads"]
        if self.host:
            return self.host.downloads
        return None
    
    @property
    def downloads(self):
        total = 0
        data = self.downloads_data()
        for elem in data:
            total += elem["downloads"]
        return total

    @property
    def contributor_count(self):
        if self.host:
            return self.host.contributor_count
        return len(self.repo["users"])

    @property
    def maintainer_count(self):
        if self.host:
            return self.host.maintainer_count
        return len(self.repo["maintainers"])

    @property
    def license(self):
        if self.host:
            return self.host.license
        return bool(self.repo["license"])

    @property
    def forks(self):
        if self.host:
            return self.host.forks
        return len(self.repo["users"])

    @property
    def dependents_count(self):
        if self.host:
            return self.host.forks
        return len(self.repo["users"])
