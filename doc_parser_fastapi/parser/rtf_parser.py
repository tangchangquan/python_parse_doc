from striprtf.striprtf import rtf_to_text

def parse_rtf(file_path):
    """Parse RTF files and extract text content"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            rtf_content = f.read()
        
        text = rtf_to_text(rtf_content)
        return text.strip()
        
    except Exception as e:
        raise ValueError(f"Failed to parse RTF file: {str(e)}") 