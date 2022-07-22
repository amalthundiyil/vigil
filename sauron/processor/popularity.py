from urllib.parse import urlparse
from enum import Enum

from github import Github

from sauron.processor.managers.pypi import Pypi
from sauron.processor.managers.npm import Npm
from sauron.processor.hosts.github import Github

class PopularityTypes(str, Enum):
    github = "github"
    npm = "npm"
    pypi = "pypi"

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
            p = Npm.from_url(url, token)
        elif netloc == cls.GITHUB_URL:
            p = Github.from_url(url, token)
        elif netloc == cls.PYPI_URL:
            p = Pypi.from_url(url, token)
        return p

    @classmethod
    def from_name(cls, name, type, token) -> None:
        p = None
        if type == PopularityTypes.npm:
            p = Npm.from_name(name, token)
        elif type == PopularityTypes.github:
            p = Github.from_name(name, token)
        elif type == PopularityTypes.pypi:
            p = Pypi.from_name(name, token)
        return p

    def process(self):
        raise NotImplementedError("No popularity processor for given identifiers.")
    
    def get_download_count(self, data):
        raise NotImplementedError("No popularity processor for given identifiers.")
