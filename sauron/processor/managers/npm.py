from urllib.parse import urlparse

import requests

from sauron.processor.hosts.github import Github
from sauron.processor.base_backend import BackendTypes, BaseBackend


class Npm(BaseBackend):
    def __init__(self, name, token=None) -> None:
        self.name = name
        self.type = BackendTypes.npm
        self.token = token
        self.repo = self.get_repo()
        self.host = self.get_repository()
        self.result = {}

    @classmethod
    def from_url(cls, url, token):
        import pdb; pdb.set_trace()
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
            return Github.from_url(url, self.token)


    @property
    def downloads(self):
        r = requests.get(f"https://api.npmjs.org/downloads/range/last-week/{self.name}")
        if r.status_code < 400 and r.status_code >= 200:
            obj = r.json()
            return obj["downloads"]
        if type(self.host) == Github:
            return self.host.downloads
        return None

    @property
    def forks(self):
        if type(self.host) == Github:
            return self.host.forks
        return None

    @property
    def contributor_count(self):
        if type(self.host) == Github:
            return self.host.contributor_count
        return len(self.repo["users"])

    @property
    def maintainer_count(self):
        if type(self.host) == Github:
            return self.host.maintainer_count
        return len(self.repo["maintainers"])

    @property
    def created_since(self):
        if type(self.host) == Github:
            return self.host.created_since
        return None

    @property
    def updated_since(self):
        if type(self.host) == Github:
            return self.host.updated_since
        return None

    @property
    def commit_frequency(self):
        if type(self.host) == Github:
            return self.host.commit_frequency
        return None

    @property
    def comment_frequency(self):
        if type(self.host) == Github:
            return self.host.comment_frequency
        return None

    @property
    def closed_issues_count(self):
        if type(self.host) == Github:
            return self.host.closed_issues_count
        return None

    @property
    def updated_issues_count(self):
        if type(self.host) == Github:
            return self.host.updated_issues_count
        return None
 

    @property
    def code_review_count(self):
        if type(self.host) == Github:
            return self.host.code_review_count
        return None
    
    @property
    def issue_age(self):
        if type(self.host) == Github:
            return self.host.issue_age
        return None

    @property
    def comments(self):
        if type(self.host) == Github:
            return self.host.comments
        return None
    
    @property
    def org_count(self):
        if type(self.host) == Github:
            return self.host.org_count
        return None
    
    @property
    def license(self):
        if type(self.host) == Github:
            return self.host.license
        return bool(self.repo["license"])

    @property
    def code_of_conduct(self):
        if type(self.host) == Github:
            return self.host.code_of_conduct
        return None


    @property
    def bus_factor(self):
        if type(self.host) == Github:
            return self.host.bus_factor
        return None

    @property
    def forks(self):
        if type(self.host) == Github:
            return self.host.forks
        return len(self.repo["users"])

    @property
    def reactions_count(self):
        if type(self.host) == Github:
            return self.host.forks
        return None
    
    @property
    def stars_count(self):
        if type(self.host) == Github:
            return self.host.stars_count
        return None


    @property
    def followers_count(self):
        if type(self.host) == Github:
            return self.host.followers_count
        return None

    @property
    def watchers_count(self):
        if type(self.host) == Github:
            return self.host.watchers_count
        return None

    @property
    def dependents_count(self):
        return len(self.repo["users"])
