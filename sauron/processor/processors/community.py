from sauron.processor.base_processor import BaseProcessor
from sauron.processor.metrics import community


class CommunityProcessor(BaseProcessor):
    def get_activity_score(self):
        data = {
            "maintainer_count": self.backend.maintainer_count,
            "org_count": self.backend.org_count,
            "contributor_count": self.backend.contributor_count,
            "dependents_count": self.backend.dependents_count,
            "bus_factor": self.backend.bus_factor,
        }
        return community.summarize_score(data)

    def get_activity_description(self):
        return community.summarize_description()

    def get_activity(self):
        activity = {
            "score": self.get_activity_score(),
            "description": self.get_activity_description(),
        }
        return activity

    def summarize(self, data):
        return self.data

    def process(self):
        activity = self.get_activity()
        self.data = [{"community_activity": activity}]
        return self.data
