import math

WEIGHTS = {
"maintainer_count" : 0.2090,
"contributor_count" : 0.18009,
"org_count" : 0.11501,
"dependents_count" : 0.3090,
"license" : 0.06010,
"code_of_conduct" : 0.06010,
"bus_factor" : 0.0604
}

# Max thresholds for various parameters.
THRESHOLDS = {
"maintainer_count" : 1000,
"contributor_count" : 1000,
"org_count" : 10,
"dependents_count" : 500000,
"license" : 1,
"code_of_conduct" : 1,
"bus_factor" : 1000
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
    total_weight = sum([v for k, v in WEIGHTS.items()])
    total_score = 0
    for k, v in data.items():
        total_score += get_param_score(k, v)
    criticality_score = round(total_score / total_weight, 5)
    return criticality_score


def summarize_description(data):
    s = summarize_score(data)
    return f"Got score of {s}/1"
