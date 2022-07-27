import math

MAINTAINER_COUNT_ACTIVITY = 0.2090
CONTRIBUTOR_COUNT_WEIGHT_ACTIVITY = 0.18009
ORG_COUNT_WEIGHT_ACTIVITY = 0.11501
DEPENDENTS_COUNT_ACTIVITY = 500000

# Max thresholds for various parameters.
MAINTAINER_COUNT_THRESHOLD_ACTIVITY = 1000
CONTRIBUTOR_COUNT_THRESHOLD_ACTIVITY = 1000
ORG_COUNT_THRESHOLD_ACTIVITY = 10
DEPENDENTS_COUNT_THRESHOLD_ACTIVITY = 500000


def get_param_score(param, max_value, weight=1):
    """Return paramater score given its current value, max value and
    parameter weight."""
    return (math.log(1 + param) / math.log(1 + max(param, max_value))) * weight


def summarize_score(item):
    total_weight_ACTIVITY = (
        MAINTAINER_COUNT_ACTIVITY
        + ORG_COUNT_WEIGHT_ACTIVITY
        + CONTRIBUTOR_COUNT_WEIGHT_ACTIVITY
        + DEPENDENTS_COUNT_THRESHOLD_ACTIVITY
    )
    criticality_score = round(
        (
            (
                get_param_score(
                    item["maintainer_count"],
                    MAINTAINER_COUNT_THRESHOLD_ACTIVITY,
                    MAINTAINER_COUNT_ACTIVITY,
                )
            )
            + (
                get_param_score(
                    item["org_count"],
                    ORG_COUNT_THRESHOLD_ACTIVITY,
                    ORG_COUNT_WEIGHT_ACTIVITY,
                )
            )
            + (
                get_param_score(
                    item["contributor_count"],
                    CONTRIBUTOR_COUNT_THRESHOLD_ACTIVITY,
                    CONTRIBUTOR_COUNT_WEIGHT_ACTIVITY,
                )
            )
            + (
                get_param_score(
                    item["dependents_count"],
                    DEPENDENTS_COUNT_THRESHOLD_ACTIVITY,
                    DEPENDENTS_COUNT_ACTIVITY,
                )
            )
        )
        / total_weight_ACTIVITY,
        5,
    )
    return criticality_score


def summarize_description():
    return ""
