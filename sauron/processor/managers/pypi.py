from urllib.parse import urlparse

import requests

from sauron.processor.hosts.github import Github

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

    def stargazers(self):
        if type(self.g) == Github:
            self.result.update({"stargazers" :self.g.stargazers()})

    def downloads(self):
        r = requests.get(f"https://api.npmjs.org/downloads/range/last-week/{self.name}")
        if r.status_code < 400 and r.status_code >= 200:
            obj = r.json()
            self.result.update({"downloads": obj["downloads"]})
    
    def get_download_count(self, data):
        total = 0
        for download in data["downloads"]:
            total += download["downloads"]
        data["downloads"] = total
        return data


    def forks(self):
        if type(self.g) == Github:
            self.result.update({"forks":self.g.forks()})

    def contributors(self):
        if type(self.g) == Github:
            self.result.update({"contributors":self.g.contributors()})
        else:
            self.result.update({"contributors": len(self.repo["users"])})

    def dependents(self):
        return len(self.repo["users"])
    
    def process(self):
        self.stargazers(),
        self.downloads(),
        self.contributors(),
        self.forks()
        self.dependents(),
        return self.result

