from urllib.parse import urlparse
from datetime import datetime

from github import Github as PyGithub

class Github():

    def __init__(self, owner, repository, token=None) -> None:
        self.g = PyGithub(token)
        self.name = f"{owner}/{repository}"
        self.repo = self.g.get_repo(self.name)
    
    @classmethod
    def from_url(cls, url, token):
        repo_url = urlparse(url).path[1:]
        owner, repo = repo_url.split("/")
        if repo.endswith(".git"):
            repo = repo[:-4]
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
            data = {"downloads":0, "day": release.created_at}
            data["day"] = datetime.strftime(data["day"], '%Y-%m-%d-%H-%M')
            for asset in release.get_assets():
                data["downloads"] += asset.download_count
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

