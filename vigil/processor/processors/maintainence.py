from vigil.processor.base_processor import BaseProcessor
from vigil.processor.metrics import maintainence


class MaintainenceProcessor(BaseProcessor):
    def summarize(self):
        data = {
            "updated_since": self.backend.updated_since,
            "created_since": self.backend.created_since,
            "commit_frequency": self.backend.commit_frequency,
            "comment_frequency": self.backend.comment_frequency,
            "closed_issues_count": self.backend.closed_issues_count,
            "updated_issues_count": self.backend.updated_issues_count,
            "code_review_count": self.backend.code_review_count,
            "issue_age": self.backend.issue_age,
        }
        res = {
            "score": maintainence.summarize_score(data),
            "description": maintainence.summarize_description(data),
        }
        return res

    def process(self):
        data = {
            "updated_since": self.backend.updated_since,
            "created_since": self.backend.created_since,
            "commit_frequency": self.backend.commit_frequency,
            "comment_frequency": self.backend.comment_frequency,
            "closed_issues_count": self.backend.closed_issues_count,
            "updated_issues_count": self.backend.updated_issues_count,
            "code_review_count": self.backend.code_review_count,
            "issue_age": self.backend.issue_age,
        }
        metrics = []
        scores = []
        descs = []
        for k, v in data.items():
            metrics.append(k)
            scores.append(maintainence.get_param_score(k, v))
            descs.append(maintainence.get_param_description(k, v))
        return {"metrics": metrics, "score": scores, "description": descs}

    def server_ts(self):
        data = {"commit_frequency": self.backend.commit_frequency_data()}
        return data
