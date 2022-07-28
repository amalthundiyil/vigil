from sauron.processor.base_processor import BaseProcessor
from sauron.processor.metrics import  popularity


class PopularityProcessor(BaseProcessor):
    def get_activity_score(self):
        data = {
            "watchers_count": self.backend.watchers_count,
            "stars_count": self.backend.stars_count,
            "followers_count": self.backend.followers_count,
            "reactions_count": self.backend.reactions_count,
            "dependents_count": self.backend.dependents_count,
        }
        return popularity.summarize_score(data)

    def get_activity_description(self):
        return popularity.summarize_description()

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
        self.data = [{"activity": activity}]
        return self.data
