from urllib.parse import urlparse

import requests

from sauron.processor.hosts.github import Github


class Npm:
    def __init__(self, name, token=None) -> None:
        self.name = name
        self.token = token
        self.repo = self.get_repo()
        self.get_repository()
        self.result = {}

    @classmethod
    def from_url(cls, url, token):
        if url.endswith("/"):
            url = url[:-1]
        repo_url = urlparse(url).path[1:]
        owner, repo = repo_url.split("/")
        return cls(owner, repo, token)

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
            self.g = Github.from_url(url, self.token)

    @property
    def stargazers(self):
        if type(self.g) == Github:
            return self.g.stargazers
        return None

    @property
    def downloads(self):
        r = requests.get(f"https://api.npmjs.org/downloads/range/last-week/{self.name}")
        if r.status_code < 400 and r.status_code >= 200:
            obj = r.json()
            return obj["downloads"]
        if type(self.g) == Github:
            return self.g.downloads
        return None

    @property
    def forks(self):
        if type(self.g) == Github:
            return self.g.forks
        return None

    @property
    def contributor_count(self):
        if type(self.g) == Github:
            return self.g.contributor_count
        return len(self.repo["users"])

    @property
    def dependents_count(self):
        return len(self.repo["users"])
