import docx2txt

def parse_doc(file_path):
    """Parse legacy DOC files using docx2txt library"""
    try:
        return docx2txt.process(file_path)
    except Exception as e:
        raise ValueError(f"Failed to parse DOC file: {str(e)}") 