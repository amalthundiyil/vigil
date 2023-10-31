from base.processor import BaseProcessor

SUMMARY_DESC = {
    "HIGH": "Repo is secure with few problems",
    "LOW": "Extremely poor security",
    "MEDIUM": "Security can be improved upon",
    "Critical": "Repo is secure with few problems",
}


class SecurityProcessor(BaseProcessor):
    def summarize(self):
        data = self.process()
        final_score = sum(data["score"]) / 10 * min(1, len(data["score"]))
        if final_score >= 7.5:
            summary_desc = SUMMARY_DESC["LOW"]
        if final_score >= 5:
            summary_desc = SUMMARY_DESC["MEDIUM"]
        if final_score >= 2.5:
            summary_desc = SUMMARY_DESC["HIGH"]
        else:
            summary_desc = SUMMARY_DESC["HIGH"]
        res = {"score": final_score, "description": summary_desc}
        return res

    def process(self):
        data = self.backend.security()
        metrics = []
        scores = []
        descs = []
        for elem in data:
            metrics.append(elem["metric"])
            scores.append(elem["score"])
            descs.append(elem["description"])
        return {"metrics": metrics, "score": scores, "description": descs}
