from sauron.processor.base_processor import BaseProcessor
from sauron.processor.metrics import maintainence 


class MaintainenceProcessor(BaseProcessor):
    def get_activity_score(self):
        data = {
            "updated_since": self.backend.updated_since,
            "created_since": self.backend.created_since,
            "commit_frequency": self.backend.commit_frequency,
            "comment_frequency": self.backend.comment_frequency,
            "closed_issues_count": self.backend.closed_issues_count,
            "updated_issues_count": self.backend.updated_issues_count,
            "code_review_count": self.backend.code_review_count,
            "issue_age": self.backend.issue_age,
            "downloads": self.backend.downloads,
        }
        return maintainence.summarize_score(data)

    def get_activity_description(self):
        return maintainence.summarize_description()

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
        self.data = [{"maintainence_activity": activity}]
        return self.data
