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
    "followup_actions",
}

FIELD_MAPPING = {
    "doctor": "hcp_name",
    "Doctor": "hcp_name",
    "disease": "topics_discussed",
    "Disease": "topics_discussed",
    "condition": "topics_discussed",
    "Condition": "topics_discussed",
    "treatment": "materials_shared",
    "Samples Distributed": "samples_distributed",
    "samples distributed": "samples_distributed",
}

LIST_FIELDS = {
    "attendees",
    "topics_discussed",
    "materials_shared",
    "samples_distributed",
    "followup_actions",
}

VALID_INTERACTIONS = {"visit", "call", "meeting"}

FIELD_STRATEGY = {
    "hcp_name": "overwrite",
    "interaction_type": "overwrite",
    "date": "resolve_date",
    "time": "overwrite",
    "attendees": "smart_replace",
    "topics_discussed": "smart_replace",
    "materials_shared": "merge",
    "samples_distributed": "merge_objects",
    "sentiment": "overwrite",
    "outcomes": "overwrite",
    "followup_actions": "merge"
}

def is_empty(value):
    return value in [None, "", [], {}]

def sanitize_payload(payload):
    if "interaction_type" in payload:
        if payload["interaction_type"] not in VALID_INTERACTIONS:
            del payload["interaction_type"]
    return payload


def normalize_payload_types(payload: dict):
    for key in LIST_FIELDS:
        if key in payload:
            if isinstance(payload[key], str):
                payload[key] = [payload[key]]
    return payload


def normalize_payload(payload: dict):
    normalized = {}
    for key, value in payload.items():
        mapped_key = FIELD_MAPPING.get(key, key)
        normalized[mapped_key] = value
    return normalized


def filter_payload(payload: dict):
    return {
        k: v
        for k, v in payload.items()
        if k.lower() in {f.lower() for f in ALLOWED_FIELDS}
    }

from datetime import datetime, timedelta
import re

def resolve_date(value: str):
    if not value:
        return value

    value = value.lower().strip()
    today = datetime.now()

    if "today" in value:
        return today.strftime("%Y-%m-%d")

    if "yesterday" in value:
        return (today - timedelta(days=1)).strftime("%Y-%m-%d")

    if "tomorrow" in value:
        return (today + timedelta(days=1)).strftime("%Y-%m-%d")

    return value  # fallback

def smart_replace(existing, new):
    # If LLM clearly means correction → replace
    return new

def merge_lists(existing, new):
    existing = existing if isinstance(existing, list) else []

    if new is None:
        return existing

    if not isinstance(new, list):
        new = [new]

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
            "quantity": s.get("quantity") or s.get("Samples Distributed"),
        })
    return normalized


import copy
from datetime import datetime, timedelta
from app.services.pdf_generator import generate_samples_pdf

# def apply_action(form: dict, action: str, payload: dict):
#     if not action:
#         return form
#     updated_form = copy.deepcopy(form)
#     payload = payload or {}
#     if action == "DELETE":
#         payload = normalize_payload(payload)
#         payload = filter_payload(payload)

#         for key, value in payload.items():

#             if value in [None, "", "unknown"]:
#                 continue


#             is_delete_all = str(value).lower() in ["all", "__all__", "remove all", "*", "clear all", "delete all"]


#             # for multi value fields

#             if key in LIST_FIELDS:

#                 existing = updated_form.get(key, [])

#                 if not isinstance(existing, list):
#                     existing = []

#                 #  1: delete ALL
#                 if is_delete_all:
#                     updated_form[key] = []

#                 #  2: delete specific value(s)
#                 else:

#                     # confirm list format for safety
#                     if not isinstance(value, list):
#                         value = [value]

#                     updated_form[key] = [
#                         item for item in existing
#                         if item not in value
#                     ]

#             
#             # delete logic for single values
#             else:

#                 # CASE 1: delete ALL OR any delete request → clear field
#                 updated_form[key] = None
#         return updated_form
    

#     if action == "GENERATE_ARTIFACT":
#         file_path = generate_samples_pdf(payload)

#         updated_form["generated_artifact"] = {
#             "type": "pdf",
#             "path": file_path
#         }


#     
#     # 1. normalization of the samples 

#     if "samples_distributed" in payload:
#         payload["samples_distributed"] = normalize_samples(
#             payload["samples_distributed"]
#         )

#     
#     # 2. Normalization of the keys
#   
#     payload = normalize_payload(payload)

#   
#     # 3. filter after normalization
#   
#     payload = filter_payload(payload)

# 
#     # 4. sanitize
#    
#     payload = sanitize_payload(payload)

#    
#     # 5. Type normalization
#     
#     payload = normalize_payload_types(payload)
#     if action == "GENERATE_ARTIFACT":

#         import os, uuid
#         from datetime import datetime

#         artifact = payload.get("samples_distributed", [])
#         print("ARTIFACT DEBUG:", artifact, type(artifact))

#         pdf_buffer = generate_samples_pdf(artifact)

#         os.makedirs("files", exist_ok=True)

#         timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
#         file_id = f"samples_{timestamp}_{uuid.uuid4().hex[:6]}.pdf"
#         file_path = f"files/{file_id}"

#         with open(file_path, "wb") as f:
#             f.write(pdf_buffer.getvalue())

#         artifact_file = f"http://127.0.0.1:8000/files/{file_id}"

#         updated_form["artifact_file"] = artifact_file

#         return {
#             "form": updated_form,
#             "action": action,
#             "artifact_file": artifact_file,
#             "message": "Artifact generated successfully"
#         }

#     if action not in ["ADD", "UPDATE"]:
#         return updated_form

#     #  if payload becomes empty,then stop
#     if not payload:
#         print("WARNING: empty payload after processing")
#         return updated_form

#     for key, value in payload.items():

#         # skip invalid values
#         if value in [None, "", "unknown"]:
#             continue

#         strategy = FIELD_STRATEGY.get(key, "merge")

#         if strategy == "overwrite":
#             updated_form[key] = value

#         elif strategy == "resolve_date":
#             updated_form[key] = resolve_date(value)

#         elif strategy == "smart_replace":
#             updated_form[key] = value

#         elif strategy == "merge":
#             existing = updated_form.get(key, [])
#             updated_form[key] = merge_lists(existing, value)

#         elif strategy == "merge_objects":
#             existing = updated_form.get(key, [])
#             updated_form[key] = merge_lists(existing, value)

#         else:
#             updated_form[key] = value

#         # sync rule
#         if key == "hcp_name":
#             updated_form["attendees"] = [value]

#     return updated_form


def apply_action(form: dict, action: str, payload: dict):
    if not action:
        return form

    action = action.upper()
    updated_form = copy.deepcopy(form)
    payload = payload or {}


    # DELETE ACTION
    
    if action == "DELETE":

        payload = normalize_payload(payload)
        payload = filter_payload(payload)

        for key, value in payload.items():

            
            if key not in payload:
                continue

            # interpret delete intent 
            is_delete_all = str(value).lower() in [
                "all", "__all__", "remove all", "*", "clear all", "delete all"
            ]

            
            # if the key is in the list fields

            if key in LIST_FIELDS:

                existing = updated_form.get(key, [])
                if not isinstance(existing, list):
                    existing = []

                if is_delete_all:
                    updated_form[key] = []
                else:
                    if value is None:
                        continue

                    if not isinstance(value, list):
                        value = [value]

                    updated_form[key] = [
                        item for item in existing
                        if item not in value
                    ]

            
            # deletion of scalar fields (fields having a single valye (date/TIme))
            
            else:

                updated_form[key] = None

        return updated_form
    
   
    
    # if action == "GENERATE_ARTIFACT":

    #     artifact = payload.get("samples_distributed", [])

    #     pdf_buffer = generate_samples_pdf(artifact)

    #     import os, uuid
    #     from datetime import datetime

    #     os.makedirs("files", exist_ok=True)

    #     timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    #     file_id = f"samples_{timestamp}_{uuid.uuid4().hex[:6]}.pdf"
    #     file_path = f"files/{file_id}"

    #     with open(file_path, "wb") as f:
    #         f.write(pdf_buffer.getvalue())

    #     artifact_file = f"http://127.0.0.1:8000/files/{file_id}"

    #     updated_form["generated_artifact"] = {
    #         "type": "pdf",
    #         "path": file_path
    #     }

    #     updated_form["artifact_file"] = artifact_file

    #     return {
    #         "form": updated_form,
    #         "action": action,
    #         "artifact_file": artifact_file,
    #         "message": "Artifact generated successfully"
    #     }
    if action == "GENERATE_ARTIFACT":

        artifact_data = normalize_samples(
            payload.get("samples_distributed", [])
        )

        pdf_buffer = generate_samples_pdf(artifact_data)

        import os, uuid
        from datetime import datetime

        os.makedirs("files", exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        file_id = f"samples_{timestamp}_{uuid.uuid4().hex[:6]}.pdf"
        file_path = f"files/{file_id}"

        with open(file_path, "wb") as f:
            f.write(pdf_buffer.getvalue())

        artifact_file = f"http://127.0.0.1:8000/files/{file_id}"
        
        return {
            "form": updated_form,
            "action": action,
            "artifact_file": artifact_file,
            "message": "Artifact generated successfully"
        }
  
    # add / update actions
    
    if action not in ["ADD", "UPDATE"]:
        return updated_form

#  normalize pipeline 
    if "samples_distributed" in payload:
        payload["samples_distributed"] = normalize_samples(
            payload["samples_distributed"]
        )

    payload = normalize_payload(payload)
    payload = filter_payload(payload)
    payload = sanitize_payload(payload)
    payload = normalize_payload_types(payload)

    if not payload:
        return updated_form



    for key, value in payload.items():

        if is_empty(value):
            continue

        strategy = FIELD_STRATEGY.get(key, "merge")

        #  Updation logic for scalar fields 
        if key not in LIST_FIELDS:

            if strategy == "overwrite":
                updated_form[key] = value

            elif strategy == "resolve_date":
                updated_form[key] = resolve_date(value)

            else:
                updated_form[key] = value

        
        else:

            existing = updated_form.get(key, [])

            if not isinstance(existing, list):
                existing = []

            if not isinstance(value, list):
                value = [value]

            # strict append (no replacement logic)
            for item in value:
                if item not in existing:
                    existing.append(item)

            updated_form[key] = existing

        # sync rule
        if key == "hcp_name":
            updated_form["attendees"] = [value]

    return updated_form