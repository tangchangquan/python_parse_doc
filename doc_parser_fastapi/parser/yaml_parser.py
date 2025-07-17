import yaml

def parse_yaml(file_path):
    """Parse YAML files and convert to readable text format"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        
        # Convert YAML data back to formatted string
        return yaml.dump(data, default_flow_style=False, allow_unicode=True)
        
    except yaml.YAMLError as e:
        raise ValueError(f"Failed to parse YAML file - invalid YAML format: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to parse YAML file: {str(e)}") 