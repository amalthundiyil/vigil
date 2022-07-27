from sauron.processor.base_processor import BaseProcessor
from sauron.processor.metrics import community


class CommunityProcessor(BaseProcessor):
    def get_activity_score(self):
        data = {
            "updated_since": self.backend.updated_since,
            "created_since": self.backend.created_since,
            "maintainer_count": self.backend.maintainer_count,
            "contributor_count": self.backend.contributor_count,
            "commit_frequency": self.backend.commit_frequency,
            "comment_frequency": self.backend.comment_frequency,
            "closed_issues_count": self.backend.closed_issues_count,
            "updated_issues_count": self.backend.updated_issues_count,
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
