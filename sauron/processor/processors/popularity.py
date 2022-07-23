from urllib.parse import urlparse

from github import Github

from sauron.processor.managers.pypi import Pypi
from sauron.processor.managers.npm import Npm
from sauron.processor.hosts.github import Github
from sauron.processor import BackendTypes, BackendUrls


class PopularityProcessor:

    name = None
    url = None

    @classmethod
    def from_url(cls, url, token) -> None:
        p = None
        netloc = urlparse(url).netloc
        if netloc == BackendUrls.npm_url:
            p = Npm.from_url(url, token)
        elif netloc == BackendUrls.github_url:
            p = Github.from_url(url, token)
        elif netloc == BackendUrls.pypi_url:
            p = Pypi.from_url(url, token)
        return p

    @classmethod
    def from_name(cls, name, type, token) -> None:
        p = None
        if type == BackendTypes.npm:
            p = Npm.from_name(name, token)
        elif type == BackendTypes.github:
            p = Github.from_name(name, token)
        elif type == BackendTypes.pypi:
            p = Pypi.from_name(name, token)
        return p

    def process(self):
        raise NotImplementedError("No popularity processor for given identifiers.")

    def get_download_count(self, data):
        raise NotImplementedError("No popularity processor for given identifiers.")
