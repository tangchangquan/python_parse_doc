import os
import tempfile
import requests
import urllib.parse

from .docx_parser import parse_docx
from .doc_parser import parse_doc
from .pdf_parser import parse_pdf
from .txt_parser import parse_txt
from .csv_parser import parse_csv
from .html_parser import parse_html
from .xml_parser import parse_xml
from .rtf_parser import parse_rtf
from .epub_parser import parse_epub
from .json_parser import parse_json
from .yaml_parser import parse_yaml

SUPPORTED_EXTENSIONS = {
    '.docx': 'Microsoft Word Document',
    '.doc': 'Microsoft Word Document (Legacy)',
    '.pdf': 'Portable Document Format',
    '.txt': 'Plain Text',
    '.text': 'Plain Text',
    '.csv': 'Comma Separated Values',
    '.html': 'HyperText Markup Language',
    '.htm': 'HyperText Markup Language',
    '.xml': 'Extensible Markup Language',
    '.rtf': 'Rich Text Format',
    '.epub': 'Electronic Publication',
    '.json': 'JavaScript Object Notation',
    '.yaml': 'YAML Ain\'t Markup Language',
    '.yml': 'YAML Ain\'t Markup Language'
}

def validate_file_type(file_path):
    """Validate if the file type is supported"""
    ext = os.path.splitext(file_path)[-1].lower()
    if ext not in SUPPORTED_EXTENSIONS:
        supported_list = ', '.join(SUPPORTED_EXTENSIONS.keys())
        raise ValueError(f"Unsupported file type: {ext}. Supported formats: {supported_list}")
    return ext

def download_file(url):
    """Download file from URL with better error handling"""
    try:
        # Add user agent to avoid blocks
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, timeout=30, headers=headers)
        response.raise_for_status()
        
        # Extract filename and decode it
        raw_filename = url.split("/")[-1].split("?")[0]
        filename = urllib.parse.unquote(raw_filename)
        
        if not filename:
            filename = "downloaded_file"
        
        suffix = os.path.splitext(filename)[-1]
        if not suffix:
            raise ValueError("Cannot determine file type from URL")
        
        # Validate file type before downloading
        validate_file_type(filename)
        
        tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        tmp.write(response.content)
        tmp.close()
        return tmp.name
        
    except requests.exceptions.Timeout:
        raise Exception("File download timed out")
    except requests.exceptions.ConnectionError:
        raise Exception("Connection error during file download")
    except requests.exceptions.HTTPError as e:
        raise Exception(f"HTTP error during file download: {e}")
    except Exception as e:
        if "Unsupported file type" in str(e):
            raise e
        raise Exception(f"File download failed: {str(e)}")

def parse_file(file_path):
    """Parse file with enhanced error handling"""
    if not os.path.exists(file_path):
        raise ValueError("File does not exist")
    
    if os.path.getsize(file_path) == 0:
        raise ValueError("File is empty")
    
    ext = validate_file_type(file_path)

    try:
        if ext == ".docx":
            return parse_docx(file_path)
        elif ext == ".doc":
            return parse_doc(file_path)
        elif ext == ".pdf":
            return parse_pdf(file_path)
        elif ext in [".txt", ".text"]:
            return parse_txt(file_path)
        elif ext == ".csv":
            return parse_csv(file_path)
        elif ext in [".html", ".htm"]:
            return parse_html(file_path)
        elif ext == ".xml":
            return parse_xml(file_path)
        elif ext == ".rtf":
            return parse_rtf(file_path)
        elif ext == ".epub":
            return parse_epub(file_path)
        elif ext == ".json":
            return parse_json(file_path)
        elif ext in [".yaml", ".yml"]:
            return parse_yaml(file_path)
    except Exception as e:
        file_type = SUPPORTED_EXTENSIONS.get(ext, "Unknown")
        raise ValueError(f"Failed to parse {file_type} file: {str(e)}")

# 定义一个函数，用于从URL中解析文件
def parse_from_url(url):
    """Parse document from URL with comprehensive error handling"""
    if not url or not url.strip():
        raise ValueError("URL cannot be empty")
    
    # 下载文件
    file_path = download_file(url)
    try:
        # 解析文件
        content = parse_file(file_path)
        if not content or not content.strip():
            raise ValueError("Document appears to be empty or contains no extractable text")
        return content
    finally:
        # 删除文件
        try:
            os.unlink(file_path)
        except OSError:
            pass  # Ignore errors when cleaning up temp files

def parse_uploaded_file(upload_file):
    """Parse uploaded file with enhanced validation"""
    if not upload_file.filename:
        raise ValueError("No filename provided")
    
    # Decode filename if URL encoded
    decoded_filename = urllib.parse.unquote(upload_file.filename)
    suffix = os.path.splitext(decoded_filename)[-1]
    
    if not suffix:
        raise ValueError("Cannot determine file type from filename")
    
    # Validate file type
    validate_file_type(decoded_filename)
    
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    try:
        content = upload_file.file.read()
        if not content:
            raise ValueError("Uploaded file is empty")
        
        tmp.write(content)
        tmp.close()
        
        parsed_content = parse_file(tmp.name)
        if not parsed_content or not parsed_content.strip():
            raise ValueError("Document appears to be empty or contains no extractable text")
        return parsed_content
    finally:
        try:
            os.unlink(tmp.name)
        except OSError:
            pass  # Ignore errors when cleaning up temp files
