import math

WATCHERS_COUNT_WEIGHT = 0.3090
FOLLOWERS_COUNT_WEIGHT = 0.3090
STARS_COUNT_WEIGHT = 0.3090
REACTIONS_COUNT_WEIGHT = 0.3090
DEPENDENTS_WEIGHT = 0.3090

# Max thresholds for various parameters.
WATCHERS_COUNT_THRESHOLD = 500000
FOLLOWERS_COUNT_THRESHOLD = 500000
STARS_COUNT_THRESHOLD = 500000
REACTIONS_COUNT_THRESHOLD = 500000
DEPENDENTS_THRESHOLD = 500000



def get_param_score(param, max_value, weight=1):
    """Return paramater score given its current value, max value and
    parameter weight."""
    return (math.log(1 + param) / math.log(1 + max(param, max_value))) * weight


def summarize_score(item):
    total_weight = (
        WATCHERS_COUNT_WEIGHT
        + STARS_COUNT_WEIGHT
        + FOLLOWERS_COUNT_WEIGHT
        + REACTIONS_COUNT_WEIGHT
        + DEPENDENTS_WEIGHT
    )
    criticality_score = round(
        (
            (
                get_param_score(
                    item["watchers_count"],
                    WATCHERS_COUNT_THRESHOLD,
                    WATCHERS_COUNT_WEIGHT,
                )
            )
            + (
                get_param_score(
                    item["stars_count"],
                    STARS_COUNT_THRESHOLD,
                    STARS_COUNT_WEIGHT,
                )
            )
            + (
                get_param_score(
                    item["followers_count"],
                    FOLLOWERS_COUNT_THRESHOLD,
                    FOLLOWERS_COUNT_WEIGHT,
                )
            )
            + (
                get_param_score(
                    item["reactions_count"],
                    REACTIONS_COUNT_THRESHOLD,
                    REACTIONS_COUNT_WEIGHT,
                )
            )
            + (
                get_param_score(
                    item["dependents_count"],
                    DEPENDENTS_THRESHOLD,
                    DEPENDENTS_WEIGHT,
                )
            )
        )
        / total_weight,
        5,
    )
    return criticality_score


def summarize_description():
    return ""
