import math

COMMIT_FREQUENCY_WEIGHT_ACTIVITY = 0.18009
UPDATED_SINCE_WEIGHT_ACTIVITY = -0.12742
CODE_REVIEW_COUNT_WEIGHT_ACTIVITY = 0.04919
CLOSED_ISSUES_WEIGHT_ACTIVITY = 0.04919
ISSUE_AGE_ACTIVITY = 0.04919
UPDATED_ISSUES_WEIGHT_ACTIVITY = 0.04919
COMMENT_FREQUENCY_WEIGHT_ACTIVITY = 0.07768
RECENT_RELEASES_WEIGHT_ACTIVITY = 0.03177
CREATED_SINCE_WEIGHT_ACTIVITY = 0.07768

# Max thresholds for various parameters.
CODE_REVIEW_COUNT_THRESHOLD_ACTIVITY = 15
CREATED_SINCE_THRESHOLD_ACTIVITY = 120
UPDATED_SINCE_THRESHOLD_ACTIVITY = 12
COMMIT_FREQUENCY_THRESHOLD_ACTIVITY = 1000
RECENT_RELEASES_THRESHOLD_ACTIVITY = 26
CLOSED_ISSUES_THRESHOLD_ACTIVITY = 1000
UPDATED_ISSUES_THRESHOLD_ACTIVITY = 1000
ISSUE_AGE_THRESHOLD_ACTIVITY = 1000
COMMENT_FREQUENCY_THRESHOLD_ACTIVITY = 15


def get_param_score(param, max_value, weight=1):
    """Return paramater score given its current value, max value and
    parameter weight."""
    return (math.log(1 + param) / math.log(1 + max(param, max_value))) * weight


def summarize_score(item):
    total_weight_ACTIVITY = (
        CREATED_SINCE_WEIGHT_ACTIVITY
        + UPDATED_SINCE_WEIGHT_ACTIVITY
        + CODE_REVIEW_COUNT_WEIGHT_ACTIVITY
        + COMMIT_FREQUENCY_WEIGHT_ACTIVITY
        + CLOSED_ISSUES_WEIGHT_ACTIVITY
        + UPDATED_ISSUES_WEIGHT_ACTIVITY
        + COMMENT_FREQUENCY_WEIGHT_ACTIVITY
        + RECENT_RELEASES_WEIGHT_ACTIVITY
        + ISSUE_AGE_ACTIVITY
    )
    criticality_score = round(
        (
            (
                get_param_score(
                    item["updated_since"],
                    UPDATED_SINCE_THRESHOLD_ACTIVITY,
                    UPDATED_SINCE_WEIGHT_ACTIVITY,
                )
            )
            + (
                get_param_score(
                    item["created_since"],
                    CREATED_SINCE_THRESHOLD_ACTIVITY,
                    CREATED_SINCE_WEIGHT_ACTIVITY,
                )
            )
            + (
                get_param_score(
                    item["commit_frequency"],
                    COMMIT_FREQUENCY_THRESHOLD_ACTIVITY,
                    COMMIT_FREQUENCY_WEIGHT_ACTIVITY,
                )
            )
            + (
                get_param_score(
                    item["comment_frequency"],
                    COMMENT_FREQUENCY_THRESHOLD_ACTIVITY,
                    COMMENT_FREQUENCY_WEIGHT_ACTIVITY,
                )
            )
            + (
                get_param_score(
                    item["closed_issues_count"],
                    CLOSED_ISSUES_THRESHOLD_ACTIVITY,
                    CLOSED_ISSUES_WEIGHT_ACTIVITY,
                )
            )
            + (
                get_param_score(
                    item["updated_issues_count"],
                    UPDATED_ISSUES_THRESHOLD_ACTIVITY,
                    UPDATED_ISSUES_WEIGHT_ACTIVITY,
                )
            )
            + (
                get_param_score(
                    item["code_review_count"],
                    CODE_REVIEW_COUNT_THRESHOLD_ACTIVITY,
                    CODE_REVIEW_COUNT_WEIGHT_ACTIVITY,
                )
            )
            + (
                get_param_score(
                    item["issue_age"],
                    ISSUE_AGE_THRESHOLD_ACTIVITY,
                    ISSUE_AGE_ACTIVITY,
                )
            )
            + (
                get_param_score(
                    item["downloads"],
                    RECENT_RELEASES_THRESHOLD_ACTIVITY,
                    RECENT_RELEASES_WEIGHT_ACTIVITY,
                )
            )
        )
        / total_weight_ACTIVITY,
        5,
    )
    return criticality_score


def summarize_description():
    return ""
