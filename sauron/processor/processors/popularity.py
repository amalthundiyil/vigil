from urllib.parse import urlparse

from github import Github

from sauron.processor.managers.pypi import Pypi
from sauron.processor.managers.npm import Npm
from sauron.processor.hosts.github import Github
from sauron.processor.base_backend import BackendTypes, BackendUrls


class PopularityProcessor:

    name = None
    url = None

    def process(self):
        raise NotImplementedError("No popularity processor for given identifiers.")

    def summarize(self, data):
        raise NotImplementedError("No popularity processor for given identifiers.")
