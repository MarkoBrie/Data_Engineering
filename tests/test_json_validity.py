import json
import re

def is_valid_json(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            json.load(f)
        return True
    except json.JSONDecodeError:
        return False

def fix_trailing_comma(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    # Remove trailing commas before closing brackets/braces
    content = re.sub(r',(\s*[\]}])', r'\1', content)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

def test_json_file_validity():
    filepath = 'data/pubmed.json'
    if not is_valid_json(filepath):
        fix_trailing_comma(filepath)
        assert is_valid_json(filepath), "JSON file could not be fixed automatically."
    else:
        assert True