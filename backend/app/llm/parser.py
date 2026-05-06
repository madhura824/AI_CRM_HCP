import json
import re

def clean_llm_output(text: str):
    # Remove ```json or ``` wrappers
    text = re.sub(r"```json|```", "", text)
    return text.strip()


def parse_response(text: str):
    try:
        cleaned = clean_llm_output(text)
        return json.loads(cleaned)
    except Exception as e:
        return {
            "error": "Parsing failed",
            "raw": text
        }