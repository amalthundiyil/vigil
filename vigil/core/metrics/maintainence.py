import math

WEIGHTS = {
    "commit_frequency": 0.18009,
    "updated_since": -0.12742,
    "code_review_count": 0.04919,
    "closed_issues_count": 0.04919,
    "issue_age": 0.04919,
    "updated_issues_count": 0.04919,
    "comment_frequency": 0.07768,
    "downloads": 0.03177,
    "created_since": 0.07768,
}

# Max thresholds for various parameters.
THRESHOLDS = {
    "code_review_count": 15,
    "created_since": 120,
    "updated_since": 12,
    "commit_frequency": 1000,
    "downloads": 26,
    "closed_issues_count": 1000,
    "updated_issues_count": 1000,
    "issue_age": 1000,
    "comment_frequency": 15,
}

DESCRIPTIONS = {
    "commit_frequency": {
        "HIGH": "Well maintained",
        "LOW": "Poorly maintained",
        "MEDIUM": "Maintained sometimes",
        "CRITICAL": "Well maintained",
    },
    "comment_frequency": {
        "HIGH": "You will never get heard here",
        "LOW": "Issues and pull requests get a good response",
        "MEDIUM": "You will get heard here often",
        "CRITICAL": "No thanks. You can keep your comments to yourself",
    },
    "updated_since": {
        "HIGH": "Recently updated",
        "LOW": "Updated long ago",
        "MEDIUM": "Updated some time ago",
        "CRITICAL": "Updated with the last few days",
    },
    "code_review_count": {
        "HIGH": "Many code_reviews",
        "LOW": "Few code reviews",
        "MEDIUM": "Some code reviews",
        "CRITICAL": "Many code reviews",
    },
    "closed_issues_count": {
        "HIGH": "Sizeable amount of closed issues",
        "LOW": "Most issues are open",
        "MEDIUM": "Some issues are open",
        "CRITICAL": "All issues close",
    },
    "issue_age": {
        "HIGH": "Issues are not very old",
        "LOW": "Very old issues",
        "MEDIUM": "Older issues present",
        "CRITICAL": "Issues are closed almost immediately",
    },
    "updated_issues_count": {
        "HIGH": "Issues are updated frequently",
        "LOW": "Issues are not updated at all",
        "MEDIUM": "Some issues are updated",
        "CRITICAL": "Looks like you found a blackhole",
    },
    "created_since": {
        "HIGH": "Created a some time back",
        "LOW": "Been around since centuries",
        "MEDIUM": "Created long time ago",
        "CRITICAL": "Created very recently",
    },
}

SUMMARY_DESC = {
    "HIGH": "Repo is well maintained and has active maintainers",
    "LOW": "Repo is poorly maintained and can be considered inactive",
    "MEDIUM": "Repo is dormant",
    "CRITICAL": "Repo is well maintained and has active maintainers",
}


def get_param_score(key, value):
    """Return paramater score given its current value, max value and
    parameter weight."""
    max_value = THRESHOLDS[key]
    score = math.log(1 + value) / math.log(1 + max(value, max_value))
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
