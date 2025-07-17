import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup

def parse_epub(file_path):
    """Parse EPUB files and extract text content"""
    try:
        book = epub.read_epub(file_path)
        content = []
        
        for item in book.get_items():
            if item.get_type() == ebooklib.ITEM_DOCUMENT:
                soup = BeautifulSoup(item.get_content(), 'html.parser')
                text = soup.get_text()
                if text.strip():
                    content.append(text.strip())
        
        return '\n\n'.join(content)
        
    except Exception as e:
        raise ValueError(f"Failed to parse EPUB file: {str(e)}") 