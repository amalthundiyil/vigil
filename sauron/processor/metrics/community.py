import math


WEIGHTS = {
"maintainer_count" : 0.2090,
"contributor_count" : 0.18009,
"org_count" : 0.11501,
"license" : 0.06010,
"code_of_conduct" : 0.06010,
"bus_factor" : 0.0604
}

# Max thresholds for various parameters.
THRESHOLDS = {
"maintainer_count" : 1000,
"contributor_count" : 1000,
"org_count" : 10,
"license" : 1,
"code_of_conduct" : 1,
"bus_factor" : 1000
}

DESCRIPTIONS = {
"maintainer_count" : {"HIGH": "Many maintainers",
				"LOW": "Few to no maintainers",
				"MEDIUM": "Some maintainers",
				"CRITICAL": "Active maintainer community"},
"contributor_count" : {"HIGH": "Good number of contributors",
				"LOW": "Few key contributors",
				"MEDIUM": "Some contributors",
				"CRITICAL":"Vast community of maintainers"},
"org_count" :{"HIGH": "Good number of organizations",
				"LOW": "Few organizations",
				"MEDIUM": "Some organizations",
				"CRITICAL":"Huge array of key organizations",},
"license" : {"HIGH": "A good license",
				"LOW": "No license detected",
				"MEDIUM": "Something is wrong with the license",
				"CRITICAL":"A good license"},
"code_of_conduct" : {"HIGH": "Ethical",
				"LOW": "Code of conduct must be improved",
				"MEDIUM": "Code of conduct is good, but can be improved",
				"CRITICAL":"Ethical",},
"bus_factor" :{"HIGH": "Low risk of project collapse, even if a few contributors leave",
				"LOW": "Repo dependent on only a few contributors",
				"MEDIUM": "Fairly high bus factor",
				"CRITICAL":"Low risk of project collapse, even if a few contributors leave",},

}


SUMMARY_DESC = {"HIGH": "Community is active and has a strong code of conduct",
                 "LOW":"Inactive community",
                 "MEDIUM":"Community is dormant",
                 "Critical":  "Community is active and has a strong code of conduct"}


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
        return DESCRIPTIONS[key]["LOW"]
    if score >= 5:
        return DESCRIPTIONS[key]["MEDIUM"]
    if score >= 2.5:
        return DESCRIPTIONS[key]["HIGH"]
    else:
        return DESCRIPTIONS[key]["HIGH"]


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
        return SUMMARY_DESC["LOW"]
    if score >= 5:
        return SUMMARY_DESC["MEDIUM"]
    if score >= 2.5:
        return SUMMARY_DESC["HIGH"]
    else:
        return SUMMARY_DESC["HIGH"]




