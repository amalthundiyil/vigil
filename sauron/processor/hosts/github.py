from urllib.parse import urlparse
from datetime import datetime, timedelta
import numpy as np
import operator

from github import Github as PyGithub
from codeowners import CodeOwners

from sauron.processor.base_backend import BaseBackend


class Github(BaseBackend):
    def __init__(self, owner, repository, token=None) -> None:
        from sauron.processor.base_backend import BackendUrls, BackendTypes
        self.g = PyGithub(token)
        self.name = f"{owner}/{repository}"
        self.url = f"https://{BackendUrls.github_url}/{owner}/{repository}"
        self.type = BackendTypes.github
        self.repo = self.g.get_repo(self.name)

    @classmethod
    def from_url(cls, url, token):
        if url.endswith("/"):
            url = url[:-1]
        repo_url = urlparse(url).path[1:]
        owner, repo = repo_url.split("/")
        if repo.endswith(".git"):
            repo = repo[:-4]
        return cls(owner, repo, token)
    
    def process(self):
        return {
            "stars": self.stargazers(),
            "downloads": self.downloads(),
            "forks": self.forks(),
            "contributors": self.get_contributors(),
            "dependents": self.dependents(),
        }


    def summarize(self, data):
        # counting downloads as releases for github
        data["downloads"] = data["downloads"][0]["downloads"]
        return data

    def has_file(self, filename):
        try:
            _ = self.repo.get_contents(filename)
        except Exception:
            return False
        return True

    def get_license(self):
        try:
            _ = self.repo.get_license()
        except Exception:
            return False
        return True

    def downloads_data(self):
        downloads = []
        for release in self.repo.get_releases():
            data = {"downloads": 0, "day": release.created_at}
            data["day"] = datetime.strftime(data["day"], "%Y-%m-%d-%H-%M")
            for asset in release.get_assets():
                data["downloads"] += asset.download_count
            downloads.append(data)
        return downloads

    @classmethod
    def from_name(cls, name, token):
        owner, repo = name.split("/")
        return cls(owner, repo, token)

    @property
    def stargazers(self):
        return self.repo.stargazers_count

    @property
    def downloads(self):
        total = 0
        data = self.downloads_data()
        for d in data:
            total += d["downloads"]
        return total
    
    @property
    def forks(self):
        return self.repo.forks_count

    @property
    def contributor_count(self):
        return self.repo.get_contributors().totalCount

    @property
    def maintainer_count(self):
        file = ""
        owners = 0
        if self.has_file("OWNERS"):
            file = self.repo.get_contents("OWNERS")
        elif self.has_file("CODEOWNERS"):
            file = self.repo.get_contents("OWNERS")
        if file:
            c = CodeOwners(file.content)
            owners = 0 
            for p in c.paths:
                owners += len(p[2])
        return owners

    @property
    def dependents_count(self):
        return self.repo.network_count
    
    @property
    def created_since(self):
        now = datetime.now()
        created_since = (now - self.repo.created_at).days // 30
        return created_since

    @property
    def updated_since(self):
        now = datetime.now()
        updated_since = (now - self.repo.updated_at).days // 30
        return updated_since

    @property
    def commit_frequency(self):
        data = self.repo.get_stats_participation().all
        avg_commits_per_week  = sum(data[:13]) // 13
        return avg_commits_per_week
    
    @property
    def comment_frequency(self):
        now = datetime.now()
        issue_comments = self.repo.get_issues_comments(since=(now - timedelta(days=90)))
        pr_comments = self.repo.get_pulls_comments(since=(now - timedelta(days=90)))
        return issue_comments.totalCount + pr_comments.totalCount

    @property
    def closed_issues_count(self):
        return self.repo.get_issues(state="closed").totalCount

    @property 
    def updated_issues_count(self):
        issues = self.repo.get_issues()
        issues_l = list(issues)
        sorted_issues = sorted(issues_l, key=operator.attrgetter("updated_at"), reverse=True)
        now = datetime.now()
        latest_issues = [i for i in sorted_issues if (now - i.updated_at).days <= 90]
        return len(latest_issues)

    @property
    def code_review_count(self):
        now = datetime.now()
        review_comments = self.repo.get_pulls_review_comments(since=(now - timedelta(days=90)))
        review_comments_list = list(review_comments)
        s = {}
        for r in review_comments_list:
            s[r.pull_request_url] = s.get(r.pull_request_url, 0) + 1
        if not s:
            return 0
        code_review_count = sum(s.values()) // len(s)
        return code_review_count

    @property
    def issue_age(self):
        now = datetime.now()
        issues = self.repo.get_issues(since=(now - timedelta(days=90)))
        issue_list = list(issues)
        if not issue_list:
            return 0
        issue_age = 0
        for i in issue_list:
            date_closed = datetime.now() if not i.closed_at else i.closed_at
            issue_age += (date_closed - i.created_at).days
        avg_issue_age = issue_age / len(issue_list)
        return avg_issue_age

    @property 
    def comments(self):
        return self.repo.get_comments()

    @property
    def org_count(self):
        users = self.repo.get_contributors()
        orgs = set()
        for u in users:
            for o in u.get_orgs():
                orgs.add(o)
        return len(orgs) 
    
    @property
    def license(self):
        return int(self.get_license())


    @property
    def code_of_conduct(self):
        return int(self.has_file("CODE_OF_CONDUCT") or self.has_file("CODE_OF_CONDUCT.md"))

    @property
    def bus_factor(self):
        c_stats = self.repo.get_stats_contributors()
        max_len = min(15, len(c_stats))
        sorted_c_stats = sorted(c_stats, key=operator.attrgetter("total"), reverse=True)[:max_len]
        top_commits = [u.total for u in sorted_c_stats]
        commits = sum(top_commits) // 2
        bus = 0
        for i in top_commits:
            if i > commits:
                bus += 1
        return bus

    @property
    def elephant_factor(self):
        pass