from urllib.parse import urlparse
from datetime import datetime
from github import Github

class MaintainenceProcessor:
    def __init__(self, url, token=None) -> None:
        self.repo_url = urlparse(url).path[1:]
        self.g = Github(token)
        self.repo = self.g.get_repo(self.repo_url)

    def latest_release(self):
        latest_release = self.repo.get_releases()[0].created_at
        if type(latest_release) != datetime:
            return "Eternity"
        now = datetime.now().date()
        delta = now - latest_release.date()
        return delta.days

    
    def latest_commit(self):
        latest_commit = self.repo.get_commits()[0].commit.committer.date
        if type(latest_commit) != datetime:
            return "Eternity"
        now = datetime.now().date()
        delta = now - latest_commit.date()
        return delta.days


    def process(self):
        return {
            "open_issues" : self.repo.get_issues(state="open").totalCount,
            "open_pr" : self.repo.get_pulls(state="open").totalCount,
            "latest_commit": self.latest_commit(),
            "latest_release": self.latest_release()
        }
        