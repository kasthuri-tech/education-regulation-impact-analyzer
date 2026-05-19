import json
import os

# Find absolute path of mock_data.json relative to this python file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
JSON_PATH = os.path.join(BASE_DIR, "mock_data.json")

# Load static mock structures
with open(JSON_PATH, "r", encoding="utf-8") as f:
    _data = json.load(f)

SAMPLE_DOCUMENTS = _data["SAMPLE_DOCUMENTS"]
_MOCK_ANALYSES = _data["MOCK_ANALYSES"]

def get_mock_analysis(text):
    """
    Scans the lowercase text against loaded keywords rules, returning the corresponding 
    mock analysis mapping, defaulting to the general education notification.
    """
    text_lower = text.lower()
    
    # 1. Match specific regulations
    for item in _MOCK_ANALYSES:
        keywords = item.get("keywords", [])
        if not keywords:
            continue
        for kw in keywords:
            if kw in text_lower:
                return item["analysis"]
                
    # 2. Match general fallback regulation (empty keywords array)
    for item in _MOCK_ANALYSES:
        keywords = item.get("keywords", [])
        if not keywords:
            return item["analysis"]
            
    # Default return empty if nothing matched
    return {}
