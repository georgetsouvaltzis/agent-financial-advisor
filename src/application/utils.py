import re

def extract_content_from_tags(tag_name: str, txt: str) -> str | None:
    match = re.search(f"<{tag_name}>(.*?)</{tag_name}>", txt, re.DOTALL)
    return match[1] if match else None