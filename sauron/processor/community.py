
from urllib.parse import urlparse
from datetime import datetime
import github

class CommunityProcessor:
    def __init__(self, url, token=None) -> None:
        self.repo_url = urlparse(url).path[1:]
        self.g = github.Github(token)
        self.repo = self.g.get_repo(self.repo_url)

    def contributors(self):
        return self.repo.get_contributors().totalCount
    
    def has_file(self, filename):
        try:
            _ = self.repo.get_contents(filename)
        except github.UnknownObjectException:
            return "false"
        return "true"

    def process(self):
        return {
            "has_readme" : self.has_file('README.md'),
            "has_contributing" : self.has_file('CONTRIBUTING.md'),
            "has_code_of_conduct": self.has_file('CODE_OF_CONDUCT.md'),
            "contributors": self.contributors()
        }
        