import math

MAINTAINER_COUNT_WEIGHT = 0.2090
CONTRIBUTOR_COUNT_WEIGHT = 0.18009
ORG_COUNT_WEIGHT = 0.11501
DEPENDENTS_COUNT_WEIGHT = 0.3090
LICENSE_WEIGHT = 0.06010
CODE_OF_CONDUCT_WEIGHT = 0.06010
BUS_FACTOR = 0.0604

# Max thresholds for various parameters.
MAINTAINER_COUNT_THRESHOLD = 1000
CONTRIBUTOR_COUNT_THRESHOLD = 1000
ORG_COUNT_THRESHOLD = 10
DEPENDENTS_COUNT_THRESHOLD = 500000
LICENSE_THRESHOLD = 1
CODE_OF_CONDUCT_THRESHOLD = 1
BUS_FACTOR_THRESHOLD = CONTRIBUTOR_COUNT_THRESHOLD



def get_param_score(param, max_value, weight=1):
    """Return paramater score given its current value, max value and
    parameter weight."""
    return (math.log(1 + param) / math.log(1 + max(param, max_value))) * weight


def summarize_score(item):
    total_weight = (
        MAINTAINER_COUNT_WEIGHT
        + ORG_COUNT_WEIGHT
        + CONTRIBUTOR_COUNT_WEIGHT
        + DEPENDENTS_COUNT_WEIGHT
        + BUS_FACTOR
    )
    criticality_score = round(
        (
            (
                get_param_score(
                    item["maintainer_count"],
                    MAINTAINER_COUNT_THRESHOLD,
                    MAINTAINER_COUNT_WEIGHT,
                )
            )
            + (
                get_param_score(
                    item["org_count"],
                    ORG_COUNT_THRESHOLD,
                    ORG_COUNT_WEIGHT,
                )
            )
            + (
                get_param_score(
                    item["contributor_count"],
                    CONTRIBUTOR_COUNT_THRESHOLD,
                    CONTRIBUTOR_COUNT_WEIGHT,
                )
            )
            + (
                get_param_score(
                    item["dependents_count"],
                    DEPENDENTS_COUNT_THRESHOLD,
                    DEPENDENTS_COUNT_WEIGHT,
                )
            )
            + (
                get_param_score(
                    item["license"],
                    LICENSE_THRESHOLD,
                    LICENSE_WEIGHT,
                )
            )
            + (
                get_param_score(
                    item["code_of_conduct"],
                    CODE_OF_CONDUCT_THRESHOLD,
                    CODE_OF_CONDUCT_WEIGHT,
                )
            )
            + (
                get_param_score(
                    item["bus_factor"],
                    BUS_FACTOR_THRESHOLD,
                    BUS_FACTOR,
                )
            )
        )
        / total_weight,
        5,
    )
    return criticality_score


def summarize_description():
    return ""
