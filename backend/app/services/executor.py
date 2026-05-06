def apply_action(form: dict, action: str, payload: dict):
    updated_form = form.copy()

    if action in ["ADD", "UPDATE"]:
        for key, value in payload.items():

            # 🚫 Ignore empty values
            if value in ["", None, []]:
                continue

            if isinstance(value, list):
                existing = updated_form.get(key, [])
                updated_form[key] = list(set(existing + value))
            else:
                updated_form[key] = value

    elif action == "DELETE":
        for key, value in payload.items():
            if isinstance(updated_form.get(key), list):
                updated_form[key] = [
                    v for v in updated_form[key] if v != value
                ]
            else:
                updated_form[key] = None

    return updated_form