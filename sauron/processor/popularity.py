from urllib.parse import urlparse
from datetime import datetime
from enum import Enum

from github import Github
import requests

class PopularityTypes(str, Enum):
    github = "github"
    npm = "npm"
    pypi = "pypi"

class GithubPopularity():

    def __init__(self, owner, repository, token=None) -> None:
        self.g = Github(token)
        self.name = f"{owner}/{repository}"
        self.repo = self.g.get_repo(self.name)
    
    @classmethod
    def from_url(cls, url, token):
        repo_url = urlparse(url).path[1:]
        owner, repo = repo_url.split("/")
        return cls(owner, repo, token)
    
    @classmethod
    def from_name(cls, name, token):
        owner, repo = name.split("/")
        return cls(owner, repo, token)

    def stargazers(self):
        return self.repo.stargazers_count

    def releases(self):
        downloads = []
        for release in self.repo.get_releases():
            data = {"count":0, "created_at": release.created_at}
            data["created_at"] = datetime.strftime(data["created_at"], '%Y-%m-%d-%H-%M')
            for asset in release.get_assets():
                data["count"] += asset.download_count
            downloads.append(data)
        return downloads
    
    def get_download_count(self, data):
        # counting downloads as releases for github
        data["downloads"] = data["downloads"][0]["count"]
        return data

    def forks(self):
        return self.repo.forks_count

    def contributors(self):
        return self.repo.get_contributors().totalCount

    def dependents(self):
        return self.repo.network_count
    
    def process(self):
        return {
            "stars" : self.stargazers(),
            "downloads" : self.releases(),
            "forks" : self.forks(),
            "contributors" : self.contributors(),
            "dependents" : self.dependents(),
        }

class NpmPopularity():

    def __init__(self, name, token=None) -> None:
        self.name = name
        self.token = token
        self.repo = self.get_repo(self.name)

    @classmethod
    def from_url(cls, url, token):
        repo_url = urlparse(url).path[1:]
        owner, repo = repo_url.split("/")
        return cls(owner, repo, token)
    
    @classmethod
    def from_name(cls, name, token):
        owner, repo = name.split("/")
        return cls(owner, repo, token)
    
    def get_repo(self):
        url = f"https://registry.npmjs.org/{self.name}" 
        r = requests.get(url)
        obj = {}
        if r.status_code < 400 and r.status_code >= 200:
            obj = r.json()
        return obj 
    
    def get_repository(self):
        url = urlparse(url)
        if "github" in url.netloc:
            self.g = GithubPopularity.from_url(url, self.token)

    def stargazers(self):
        if type(self.g) == GithubPopularity:
            self.result.update({"stargazers" :self.g.stargazers()})

    def downloads(self):
        r = requests.get(f"https://api.npmjs.org/downloads/range/last-week/{self.name}")
        if r.status_code < 400 and r.status_code >= 200:
            obj = r.json()
            self.result.update({"downloads": obj["downloads"]})
    
    def get_download_count(self):
        total = 0
        for download in self.result["downloads"]:
            total += download["downloads"]
        return total


    def forks(self):
        if type(self.g) == GithubPopularity:
            self.result.update({"forks":self.g.forks()})

    def contributors(self):
        if type(self.g) == GithubPopularity:
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

class PopularityProcessor():
    NPM_URL = "npmjs.com"
    GITHUB_URL = "github.com"
    PYPI_URL = "pypi.org"
    name = None
    url = None

    def __init__(self, url, type) -> None:
        pass
    
    @classmethod
    def from_url(cls, url, token) -> None:
        p = None
        netloc = urlparse(url).netloc
        if netloc == cls.NPM_URL:
            p = NpmPopularity.from_url(url, token)
        elif netloc == cls.GITHUB_URL:
            p = GithubPopularity.from_url(url, token)
        elif netloc == cls.PYPI_URL:
            p = PypiPopularity.from_url(url, token)
        return p

    @classmethod
    def from_name(cls, name, type, token) -> None:
        p = None
        if type == PopularityTypes.npm:
            p = NpmPopularity.from_name(name, token)
        elif type == PopularityTypes.github:
            p = GithubPopularity.from_name(name, token)
        elif type == PopularityTypes.pypi:
            p = PypiPopularity.from_name(name, token)
        return p

    def process(self):
        raise NotImplementedError("No popularity processor for given identifiers.")
    
    def get_download_count(self, data):
        raise NotImplementedError("No popularity processor for given identifiers.")
