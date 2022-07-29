import math

WEIGHTS = {
"watchers_count" : 0.3090,
"followers_count" : 0.3090,
"stars_count" : 0.3090,
"reactions_count" : 0.3090,
"dependents_count" : 0.3090,
"downloads" : 0.03177,
}

# Max thresholds for various parameters.
THRESHOLDS = {
"watchers_count" : 500000,
"followers_count" : 500000,
"stars_count" : 500000,
"reactions_count" : 500000,
"dependents_count" : 500000,
"downloads" : 26,
}


def get_param_score(key, value):
    """Return paramater score given its current value, max value and
    parameter weight."""
    max_value = THRESHOLDS[key]
    weight = WEIGHTS[key]
    total = sum([v for k, v in WEIGHTS.items()])
    score = ((math.log(1 + value) / math.log(1 + max(value, max_value))) * weight) / total
    return round(score * 100, 2)

def get_summarize_param_score(key, value):
    """Return paramater score given its current value, max value and
    parameter weight."""
    max_value = THRESHOLDS[key]
    weight = WEIGHTS[key]
    return (math.log(1 + value) / math.log(1 + max(value, max_value))) * weight


def get_param_description(key, value):
    score = get_param_score(key, value)
    return f"{key} got a score of {score}"

def summarize_score(data):
    total = sum([v for k, v in WEIGHTS.items()])
    total_score = 0
    for k, v in data.items():
        total_score += get_summarize_param_score(k, v)
    criticality_score = total_score / total
    return round(criticality_score * 10, 2)


def summarize_description(data):
    s = summarize_score(data)
    return f"Got score of {s}/10"
