ALLOWED_CLAIM_STATUS = {
    "supported",
    "contradicted",
    "not_enough_information",
}

ALLOWED_SEVERITY = {
    "none",
    "low",
    "medium",
    "high",
    "unknown",
}

ALLOWED_ISSUE_TYPES = {
    "dent",
    "scratch",
    "crack",
    "glass_shatter",
    "broken_part",
    "missing_part",
    "torn_packaging",
    "crushed_packaging",
    "water_damage",
    "stain",
    "none",
    "unknown",
}

ALLOWED_RISK_FLAGS = {
    "none",
    "blurry_image",
    "cropped_or_obstructed",
    "low_light_or_glare",
    "wrong_angle",
    "wrong_object",
    "wrong_object_part",
    "damage_not_visible",
    "claim_mismatch",
    "possible_manipulation",
    "non_original_image",
    "text_instruction_present",
    "user_history_risk",
    "manual_review_required",
}

OBJECT_PART_MAP = {
    "front bumper": "front_bumper",
    "rear bumper": "rear_bumper",
    "side mirror": "side_mirror",
    "quarter panel": "quarter_panel",
    "package corner": "package_corner",
    "package side": "package_side",
}


def normalize_result(result):

    claim_status = str(
        result.get("claim_status", "not_enough_information")
    ).lower()

    if claim_status not in ALLOWED_CLAIM_STATUS:
        claim_status = "not_enough_information"

    severity = str(
        result.get("severity", "unknown")
    ).lower()

    if severity not in ALLOWED_SEVERITY:
        severity = "unknown"

    issue_type = str(
        result.get("issue_type", "unknown")
    ).lower()

    if issue_type not in ALLOWED_ISSUE_TYPES:
        issue_type = "unknown"

    object_part = str(
        result.get("object_part", "unknown")
    ).strip()

    object_part = OBJECT_PART_MAP.get(
        object_part.lower(),
        object_part.lower().replace(" ", "_")
    )

    risk_flags = result.get("risk_flags", "none")

    if isinstance(risk_flags, list):
        risk_flags = ";".join(risk_flags)

    risk_flags = str(risk_flags)

    cleaned_flags = []

    for flag in risk_flags.split(";"):
        flag = flag.strip()

        if flag in ALLOWED_RISK_FLAGS:
            cleaned_flags.append(flag)

    if not cleaned_flags:
        cleaned_flags = ["none"]

    supporting = result.get(
        "supporting_image_ids",
        "none"
    )

    if isinstance(supporting, list):
        supporting = ";".join(
            str(x) for x in supporting
        )

    if not supporting or supporting == "[]":
        supporting = "none"

    result["claim_status"] = claim_status
    result["severity"] = severity
    result["issue_type"] = issue_type
    result["object_part"] = object_part
    result["risk_flags"] = ";".join(cleaned_flags)
    result["supporting_image_ids"] = supporting

    return result