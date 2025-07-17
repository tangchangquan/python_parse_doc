import json

def parse_json(file_path):
    """Parse JSON files and convert to readable text format"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Convert JSON to formatted string
        return json.dumps(data, indent=2, ensure_ascii=False)
        
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON file - invalid JSON format: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to parse JSON file: {str(e)}") 