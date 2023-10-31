from base.processor import BaseProcessor
from metrics import community


class CommunityProcessor(BaseProcessor):
    def summarize(self):
        data = {
            "maintainer_count": self.backend.maintainer_count,
            "org_count": self.backend.org_count,
            "contributor_count": self.backend.contributor_count,
            "license": self.backend.license,
            "code_of_conduct": self.backend.code_of_conduct,
            "bus_factor": self.backend.bus_factor,
        }
        res = {
            "score": community.summarize_score(data),
            "description": community.summarize_description(data),
        }
        return res

    def process(self):
        data = {
            "maintainer_count": self.backend.maintainer_count,
            "org_count": self.backend.org_count,
            "contributor_count": self.backend.contributor_count,
            "license": self.backend.license,
            "code_of_conduct": self.backend.code_of_conduct,
            "bus_factor": self.backend.bus_factor,
        }
        metrics = []
        scores = []
        descs = []
        for k, v in data.items():
            metrics.append(k)
            scores.append(community.get_param_score(k, v))
            descs.append(community.get_param_description(k, v))
        return {"metrics": metrics, "score": scores, "description": descs}
