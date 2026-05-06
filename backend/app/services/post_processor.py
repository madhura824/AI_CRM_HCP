def enforce_action_rules(action, payload, user_input):
    text = user_input.lower()

    # DELETE conditions
    if any(word in text for word in ["remove", "delete", "clear", "don't remember"]):
        return "DELETE"

    # UPDATE conditions
    if any(word in text for word in ["sorry", "correction", "actually", "not"]):
        return "UPDATE"

    # GENERATE_ARTIFACT conditions
    if any(word in text for word in ["table", "list", "samples distributed"]):
        return "GENERATE_ARTIFACT"

    return action