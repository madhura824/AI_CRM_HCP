import copy

ALLOWED_FIELDS = {
    "hcp_name",
    "interaction_type",
    "date",
    "time",
    "attendees",
    "topics_discussed",
    "materials_shared",
    "samples_distributed",
    "sentiment",
    "outcomes",
    "followup_actions"
}

FIELD_MAPPING = {
    "doctor": "hcp_name",
    "disease": "topics_discussed",
    "condition": "topics_discussed",
    "treatment": "materials_shared"
}
LIST_FIELDS = {
    "attendees",
    "topics_discussed",
    "materials_shared",
    "samples_distributed",
    "followup_actions"
}

VALID_INTERACTIONS = {"visit", "call", "meeting"}

def sanitize_payload(payload):
    if "interaction_type" in payload:
        if payload["interaction_type"] not in VALID_INTERACTIONS:
            del payload["interaction_type"]
    return payload



def normalize_payload_types(payload: dict):
    for key in LIST_FIELDS:
        if key in payload:
            if isinstance(payload[key], str):
                payload[key] = [payload[key]]  # 🔥 convert string → list
    return payload

def normalize_payload(payload):
    normalized = {}
    for key, value in payload.items():
        mapped_key = FIELD_MAPPING.get(key, key)
        normalized[mapped_key] = value
    return normalized


def filter_payload(payload: dict):
    return {k: v for k, v in payload.items() if k in ALLOWED_FIELDS}


# def apply_action(form: dict, action: str, payload: dict):

    # updated_form = form.copy()

    # # 🔥 STEP 1: Normalize (map doctor → hcp_name)
    # payload = normalize_payload(payload)

    # # 🔥 STEP 2: Filter (remove invalid fields)
    # payload = filter_payload(payload)

    # # 🔥 STEP 3: Apply logic
    # if action in ["ADD", "UPDATE"]:
    #     for key, value in payload.items():
    #         if isinstance(value, list):
    #             existing = updated_form.get(key, [])
    #             updated_form[key] = list(set(existing + value))
    #         else:
    #             updated_form[key] = value

    # elif action == "DELETE":
    #     for key, value in payload.items():
    #         if isinstance(updated_form.get(key), list):
    #             updated_form[key] = [
    #                 v for v in updated_form[key] if v != value
    #             ]
    #         else:
    #             updated_form[key] = None

    # return updated_form
import copy

def merge_lists(existing, new):
    result = existing.copy()
    for item in new:
        if item not in result:
            result.append(item)
    return result


def apply_action(form: dict, action: str, payload: dict):
    updated_form = copy.deepcopy(form)
    payload = payload or {}

    # 🔥 STEP 1: Normalize
    payload = normalize_payload(payload)

    # 🔥 STEP 2: Sanitize
    payload = sanitize_payload(payload)

    # 🔥 STEP 3: Filter
    payload = filter_payload(payload)

    # 🔥 STEP 4: Normalize types
    payload = normalize_payload_types(payload)

    # 🔥 STEP 5: Apply logic
    if action in ["ADD", "UPDATE"]:
        for key, value in payload.items():
            if isinstance(value, list):
                existing = updated_form.get(key, [])
                updated_form[key] = merge_lists(existing, value)
            else:
                updated_form[key] = value

    elif action == "DELETE":
        for key, value in payload.items():
            if isinstance(updated_form.get(key), list):
                updated_form[key] = [
                    v for v in updated_form[key] if v != value
                ]
                if not updated_form[key]:
                    del updated_form[key]
            else:
                if key in updated_form:
                    del updated_form[key]

    return updated_form