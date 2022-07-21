
from github import Github
from urllib.parse import urlparse
from datetime import datetime


class GithubPopularity():

    def __init__(self, url, token=None) -> None:
        self.g = Github(token)
        self.repo_url = urlparse(url).path[1:]
        self.repo = self.g.get_repo(self.repo_url)

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
            "forks" : self.stargazers(),
            "contributors" : self.contributors(),
            "dependents" : self.dependents(),
        }

class NpmPopularity():
    def __init__(self) -> None:
        pass