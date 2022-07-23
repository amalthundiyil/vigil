from sauron.processor.processors.community import CommunityProcessor
from sauron.processor.processors.maintainence import MaintainenceProcessor
from sauron.processor.processors.popularity import PopularityProcessor
from sauron.processor.processors.vulns import VulnsProcessor
from sauron.processor import BackendTypes


class BaseProcessor:

    name = None
    url = None

    @classmethod
    def get_processor_class(cls, domain, url, name, type, token):
        mapping = {
            "community": CommunityProcessor,
            "maintainence": MaintainenceProcessor,
            "popularity": PopularityProcessor,
            "vulnerabilities": VulnsProcessor,
        }
        c = mapping.get(domain)
        return cls.from_input(c, url, name, type, token)

    @staticmethod
    def from_input(klass, url, name, type, token) -> None:
        validate(url, name, type)
        if name and type:
            return klass.from_name(name, type, token)
        elif url:
            return klass.from_url(url, token)

    @classmethod
    def from_url(cls, url, token) -> None:
        raise NotImplementedError("No popularity processor for given identifiers.")

    @classmethod
    def from_name(cls, name, type, token) -> None:
        raise NotImplementedError("No popularity processor for given identifiers.")

    def process(self):
        raise NotImplementedError("No popularity processor for given identifiers.")

    def summarize(self, data):
        raise NotImplementedError("No popularity processor for given identifiers.")


class ValidationError(Exception):
    def __init__(self, message="Input fields are incorrect"):
        self.message = message
        super().__init__(self.message)


def validate(url, name, type):
    if not url and (not name and not (type in BackendTypes)):
        raise ValidationError(f"Please enter either the name, type or url")
    if not url and (not name or not (type in BackendTypes)):
        raise ValidationError(f"One of name and type is invalid ({name}, {type})")
    if not url and not (name and (type in BackendTypes)):
        raise ValidationError(f"Please enter a valid URL ({url})")
