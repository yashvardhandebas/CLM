import re


def extract_profile_info(text: str):
    info = {}
    name_match = re.search(r"my name is (\w+)", text, re.I)
    if name_match:
        info["name"] = name_match.group(1)
    return info


