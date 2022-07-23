import enum


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
