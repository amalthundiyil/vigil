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

DESCRIPTIONS = {
"watchers_count" : {"HIGH": "Many watchers",
				"LOW": "Zero to no watchers",
				"MEDIUM": "Few watchers",
				"CRITICAL": "Active community of watchers"},
"followers_count" : {"HIGH": "Highly popular",
				"LOW": "Barely popular",
				"MEDIUM": "Some popularity",
				"CRITICAL":"Key ecosystem project",},
"stars_count" :{"HIGH": "Highly starred",
				"LOW": "Rarely starred",
				"MEDIUM": "Starred often",
				"CRITICAL":"Very highly starred",},
"reactions_count" : {"HIGH": "Many reactions",
				"LOW": "Few to no reactions",
				"MEDIUM": "Some reactions",
				"CRITICAL":"A lot of reactions",},
"dependents_count" : {"HIGH": "High number of dependents",
				"LOW": "Low number of dependents",
				"MEDIUM": "A few dependents",
				"CRITICAL":"Very high number of dependents"},
"downloads": {"HIGH": "Downloaded frequently",
				"LOW": "Not downloaded often",
				"MEDIUM": "Downloaded a few times",
				"CRITICAL":"Very commonly downloaded",},

}

SUMMARY_DESC = {"HIGH": "Repo is popular and downloaded frequently",
                 "LOW":"Repo is not very popular",
                 "MEDIUM":"Some downloads and interaction",
                 "CRITICAL":  "Repo is a key ecosystem project"}


def get_param_score(key, value):
    """Return paramater score given its current value, max value and
    parameter weight."""
    max_value = THRESHOLDS[key]
    score = (math.log(1 + value) / math.log(1 + max(value, max_value))) 
    return round(score * 10, 2)

def get_summarize_param_score(key, value):
    """Return paramater score given its current value, max value and
    parameter weight."""
    max_value = THRESHOLDS[key]
    weight = WEIGHTS[key]
    return (math.log(1 + value) / math.log(1 + max(value, max_value))) * weight


def get_param_description(key, value):
    score = get_param_score(key, value)
    if score >= 7.5:
        return DESCRIPTIONS[key]["CRITICAL"]
    if score >= 5:
        return DESCRIPTIONS[key]["HIGH"]
    if score >= 2.5:
        return DESCRIPTIONS[key]["MEDIUM"]
    else:
        return DESCRIPTIONS[key]["LOW"]



def summarize_score(data):
    total = sum([v for k, v in WEIGHTS.items()])
    total_score = 0
    for k, v in data.items():
        total_score += get_summarize_param_score(k, v)
    criticality_score = total_score / total
    return round(criticality_score * 10, 2)

def summarize_description(data):
    score = summarize_score(data)
    if score >= 7.5:
        return SUMMARY_DESC["CRITICAL"]
    if score >= 5:
        return SUMMARY_DESC["HIGH"]
    if score >= 2.5:
        return SUMMARY_DESC["MEDIUM"]
    else:
        return SUMMARY_DESC["LOW"]




