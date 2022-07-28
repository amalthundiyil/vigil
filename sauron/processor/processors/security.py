from sauron.processor.base_processor import BaseProcessor

class SecurityProcessor(BaseProcessor):
    def summarize(self):
        data = self.process()
        final_score =  sum(data["score"]) / min(1, len(data["score"]))
        res = {"score": final_score, "description": f"Got score of {final_score}"}
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