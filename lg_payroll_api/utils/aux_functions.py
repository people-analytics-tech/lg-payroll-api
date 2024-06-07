# This module contains auxiliary functions to transform data
import re


def clean_none_values_dict(data: dict) -> dict:
    """Remove none fields from dictionary."""

    result: dict = {}
    for key, value in data.items():
        if value != None:
            if isinstance(value, dict):
                result[key] = clean_none_values_dict(value)

            elif isinstance(value, list):
                if len(value) > 0:
                    if isinstance(value[0], dict):
                        result[key] = [clean_none_values_dict(item) for item in value]

                    else:
                        result[key] = value

                else:
                    result[key] = value

            else:
                result[key] = value

    return result


def extract_file_extension(file_name: str) -> str:
    pattern = r"\.([a-zA-Z0-9]+)$"
    match = re.search(pattern, file_name)

    if match:
        return match.group(1)
    
    else:
        return None
