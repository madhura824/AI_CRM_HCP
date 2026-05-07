import copy
from datetime import datetime

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


import copy

def merge_lists(existing, new):
    result = existing.copy()
    for item in new:
        if item not in result:
            result.append(item)
    return result

def normalize_samples(samples):
    normalized = []

    for s in samples:
        normalized.append({
            "medicine_name": s.get("medicine_name") or s.get("Medicine Name"),
            "sample_name": s.get("sample_name") or s.get("Sample Name"),
            "quantity": s.get("quantity") or s.get("Samples Distributed")
        })

    return normalized

def apply_action(form: dict, action: str, payload: dict):
    updated_form = copy.deepcopy(form)
    payload = payload or {}
    # 🔥 Normalize samples BEFORE applying
    if "samples_distributed" in payload:
        payload["samples_distributed"] = normalize_samples(
            payload["samples_distributed"]
        )

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
    elif action == "ENRICH":
        if "materials_shared" in updated_form:
            updated_form["materials_shared"] += [
                "clinical brochure",
                "research paper"
            ]
    elif action == "GENERATE_ARTIFACT":

        # priority: payload first, fallback to form
        samples = payload.get("samples_distributed") or updated_form.get("samples_distributed", [])

        if samples:
            updated_form["artifact"] = {
                "type": "samples_pdf",
                "data": samples,
                "created_at": str(datetime.now())
            }
    return updated_form