from urllib.parse import urlparse
from datetime import datetime

import requests
from tomlkit import date

from sauron.processor.hosts.github import Github
from sauron.config import setenv_from_config


class Pypi():

    def __init__(self, name, token=None) -> None:
        self.name = name
        self.token = token
        self.repo = self.get_repo()
        self.get_repository()
        self.result = {}

    @classmethod
    def from_url(cls, url, token):
        repo_url = urlparse(url).path[1:]
        owner, repo = repo_url.split("/")
        return cls(owner, repo, token)
    
    @classmethod
    def from_name(cls, name, token):
        return cls(name, token)
    
    def get_repo(self):
        setenv_from_config("libraries_api_key")
        from pybraries.search import Search
        self.search = Search()
        info = self.search.project('pypi', self.name)
        return info
    
    def get_repository(self):
        url = self.repo["repository_url"]
        parsed_url = urlparse(url)
        if "github" in parsed_url.netloc:
            self.g = Github.from_url(url, self.token)

    def stargazers(self):
        self.result.update({"stars": self.repo["stars"]})

    def downloads(self):
        r = requests.get(f"https://api.pepy.tech/api/projects/{self.name}")
        if not r.ok:
            return
        obj = r.json()
        now = datetime.now()
        downloads = []
        for k, v in obj["downloads"].items():
            dt = datetime.strptime(k, '%Y-%m-%d')
            delta = now - dt
            if delta.days <= 7:
                downloads.append({"downloads": v, "day": k})
        self.result.update({"downloads": downloads})

    def get_download_count(self, data):
        total = 0
        for download in data["downloads"]:
            for k, v in download:
                total += v
        data["downloads"] = total
        return data

    def forks(self):
        self.result.update({"forks": self.repo["forks"]})

    def contributors(self):
        d = self.search.project_contributors("pypi", self.name)
        self.result.update({"contributors": len(d)})

    def dependents(self):
        d = self.search.project_dependents("pypi", self.name)
        self.result.update({"dependents": len(d)})
    
    def process(self):
        self.stargazers(),
        self.downloads(),
        self.contributors(),
        self.forks()
        self.dependents(),
        return self.result

