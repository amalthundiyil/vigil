import enum
from urllib.parse import urlparse


class BackendEnumMeta(enum.EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        else:
            return True


class BackendTypes(str, enum.Enum, metaclass=BackendEnumMeta):
    github = "github"
    npm = "npm"
    pypi = "pypi"


class BackendUrls(str, enum.Enum, metaclass=BackendEnumMeta):
    npm_url = "npmjs.com"
    github_url = "github.com"
    pypi_url = "pypi.org"


class BaseBackend:
    name = None
    url = None
    host = None

    @classmethod
    def from_input(cls, url, name, type, token) -> None:
        from vigil.processor.base_processor import validate

        validate(url, name, type)
        if name and type:
            return cls.from_name(name, type, token)
        elif url:
            return cls.from_url(url, token)

    @classmethod
    def from_url(cls, url, token) -> None:
        from vigil.processor.hosts.github import Github
        from vigil.processor.managers.npm import Npm
        from vigil.processor.managers.pypi import Pypi

        b = None
        netloc = urlparse(url).netloc
        if BackendUrls.npm_url in netloc:
            b = Npm.from_url(url, token)
        elif BackendUrls.github_url in netloc:
            b = Github.from_url(url, token)
        elif BackendUrls.pypi_url in netloc:
            b = Pypi.from_url(url, token)
        return b

    @classmethod
    def from_name(cls, name, type, token) -> None:
        from vigil.processor.hosts.github import Github
        from vigil.processor.managers.npm import Npm
        from vigil.processor.managers.pypi import Pypi

        p = None
        if type == BackendTypes.npm:
            p = Npm.from_name(name, token)
        elif type == BackendTypes.github:
            p = Github.from_name(name, token)
        elif type == BackendTypes.pypi:
            p = Pypi.from_name(name, token)
        return p

    def get_repo(self):
        raise NotImplementedError("BaseManager cannot get repo")

    @property
    def get_downloads_data(self):
        if self.host:
            return self.host.get_downloads_data

    @property
    def commit_frequency_data(self):
        if self.host:
            return self.host.commit_frequency_data

    @property
    def downloads(self):
        if self.host:
            return self.host.downloads

    @property
    def forks(self):
        if self.host:
            return self.host.forks

    @property
    def contributor_count(self):
        if self.host:
            return self.host.contributor_count

    @property
    def maintainer_count(self):
        if self.host:
            return self.host.maintainer_count

    @property
    def created_since(self):
        if self.host:
            return self.host.created_since

    @property
    def updated_since(self):
        if self.host:
            return self.host.updated_since

    @property
    def commit_frequency(self):
        if self.host:
            return self.host.commit_frequency

    @property
    def comment_frequency(self):
        if self.host:
            return self.host.comment_frequency

    @property
    def closed_issues_count(self):
        if self.host:
            return self.host.closed_issues_count

    @property
    def updated_issues_count(self):
        if self.host:
            return self.host.updated_issues_count

    @property
    def code_review_count(self):
        if self.host:
            return self.host.code_review_count

    @property
    def issue_age(self):
        if self.host:
            return self.host.issue_age

    @property
    def comments(self):
        if self.host:
            return self.host.comments

    @property
    def org_count(self):
        if self.host:
            return self.host.org_count

    @property
    def license(self):
        if self.host:
            return self.host.license

    @property
    def code_of_conduct(self):
        if self.host:
            return self.host.code_of_conduct

    @property
    def bus_factor(self):
        if self.host:
            return self.host.bus_factor

    @property
    def forks(self):
        if self.host:
            return self.host.forks

    @property
    def reactions_count(self):
        if self.host:
            return self.host.forks

    @property
    def stars_count(self):
        if self.host:
            return self.host.stars_count

    @property
    def followers_count(self):
        if self.host:
            return self.host.followers_count

    @property
    def watchers_count(self):
        if self.host:
            return self.host.watchers_count

    @property
    def dependents_count(self):
        if self.host:
            return self.host.watchers_count

    @property
    def description(self):
        if self.host:
            return self.host.description
