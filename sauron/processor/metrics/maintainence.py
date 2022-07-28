import math

from sauron.processor.metrics.community import THRESHOLDS

WEIGHTS = {
"commit_frequency" : 0.18009,
"updated_since" : -0.12742,
"code_review_count" : 0.04919,
"closed_issues_count" : 0.04919,
"issue_age" : 0.04919,
"updated_issues_count" : 0.04919,
"comment_frequency" : 0.07768,
"downloads" : 0.03177,
"created_since" : 0.07768,
}

# Max thresholds for various parameters.
THRESHOLDS = {
"code_review_count" : 15,
"created_since" : 120,
"updated_since" : 12,
"commit_frequency" : 1000,
"downloads" : 26,
"closed_issues_count" : 1000,
"updated_issues_count" : 1000,
"issue_age" : 1000,
"comment_frequency" : 15,
}


def get_param_score(key, value):
    """Return paramater score given its current value, max value and
    parameter weight."""
    max_value = THRESHOLDS[key]
    weight = WEIGHTS[key]
    return max(0, round((math.log(1 + value) / math.log(1 + max(value, max_value))) * weight * 100, 2))

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
    criticality_score = round(total_score / total, 2)
    return round(criticality_score * 10, 2)


def summarize_description(data):
    s = summarize_score(data)
    return f"Got score of {s}/10"

