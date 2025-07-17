import xml.etree.ElementTree as ET

def parse_xml(file_path):
    """Parse XML files and extract text content"""
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        def extract_text(element):
            """Recursively extract text from XML elements"""
            text = element.text or ""
            for child in element:
                text += extract_text(child)
                if child.tail:
                    text += child.tail
            return text
        
        content = extract_text(root)
        
        # Clean up the text
        lines = [line.strip() for line in content.splitlines() if line.strip()]
        return '\n'.join(lines)
        
    except ET.ParseError as e:
        raise ValueError(f"Failed to parse XML file - invalid XML format: {str(e)}")
    except Exception as e:
        raise ValueError(f"Failed to parse XML file: {str(e)}") 