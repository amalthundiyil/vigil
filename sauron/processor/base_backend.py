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

    @classmethod
    def from_input(cls, url, name, type, token) -> None:
        from sauron.processor.base_processor import validate
        validate(url, name, type)
        if name and type:
            return cls.from_name(name, type, token)
        elif url:
            return cls.from_url(url, token)

    @classmethod
    def from_url(cls, url, token) -> None:
        from sauron.processor.hosts.github import Github
        from sauron.processor.managers.npm import Npm
        from sauron.processor.managers.pypi import Pypi
        b = None
        netloc = urlparse(url).netloc
        if netloc == BackendUrls.npm_url:
            b = Npm.from_url(url, token)
        elif netloc == BackendUrls.github_url:
            b = Github.from_url(url, token)
        elif netloc == BackendUrls.pypi_url:
            b = Pypi.from_url(url, token)
        return b

    @classmethod
    def from_name(cls, name, type, token) -> None:
        from sauron.processor.hosts.github import Github
        from sauron.processor.managers.npm import Npm
        from sauron.processor.managers.pypi import Pypi
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

