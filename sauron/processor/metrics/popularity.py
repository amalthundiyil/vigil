import math

WEIGHTS = {
"watchers_count" : 0.3090,
"followers_count" : 0.3090,
"stars_count" : 0.3090,
"reactions_count" : 0.3090,
"dependents_count" : 0.3090,
}

# Max thresholds for various parameters.
THRESHOLDS = {
"watchers_count" : 500000,
"followers_count" : 500000,
"stars_count" : 500000,
"reactions_count" : 500000,
"dependents_count" : 500000,
}



def get_param_score(key, value):
    """Return paramater score given its current value, max value and
    parameter weight."""
    max_value = THRESHOLDS[key]
    weight = WEIGHTS[key]
    return (math.log(1 + value) / math.log(1 + max(value, max_value))) * weight

def get_param_description(key, value):
    return f"{key} got a score of {value}"

def summarize_score(data):
    total = sum([v for k, v in WEIGHTS.items()])
    total_score = 0
    for k, v in data.items():
        total_score += get_param_score(k, v)
    criticality_score = round(total_score / total, 5)
    return criticality_score


def summarize_description(data):
    s = summarize_score(data)
    return f"Got score of {s}/1"


