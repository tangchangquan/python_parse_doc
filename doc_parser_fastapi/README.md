# Document Parser FastAPI

A powerful FastAPI-based document parsing service that supports multiple file formats including DOCX, DOC, PDF, HTML, XML, RTF, EPUB, JSON, YAML, CSV, and TXT files.

## Supported File Formats

- **Microsoft Word**: `.docx`, `.doc`
- **PDF**: `.pdf`
- **Text**: `.txt`, `.text`
- **Spreadsheet**: `.csv`
- **Web**: `.html`, `.htm`
- **Markup**: `.xml`
- **Rich Text**: `.rtf`
- **E-book**: `.epub`
- **Data**: `.json`, `.yaml`, `.yml`

## Features

- 📄 **Multi-format Support**: Parse 13+ different file formats
- 🌐 **URL Parsing**: Download and parse documents from URLs
- 📤 **File Upload**: Upload files directly for parsing
- 🔤 **URL Decoding**: Automatic filename URL decoding for international characters
- ⚡ **Fast API**: High-performance async API built with FastAPI
- 🐳 **Docker Ready**: Easy deployment with Docker and Docker Compose
- 🔍 **Health Checks**: Built-in health monitoring
- 📝 **Auto Documentation**: Interactive API docs at `/docs`

## Quick Start with Docker

### Option 1: Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd doc_parser_fastapi

# Start the service
docker-compose up -d

# View logs
docker-compose logs -f
```

The API will be available at `http://localhost:8080`

### Option 2: Using Docker directly

```bash
# Build the image
docker build -t doc-parser-api .

# Run the container
docker run -d \
  --name doc-parser \
  -p 8080:8080 \
  doc-parser-api
```

### Option 3: Production deployment with Nginx

```bash
# Start with Nginx reverse proxy
docker-compose --profile production up -d
```

This will start both the API and Nginx on port 80.

## API Endpoints

### Parse from URL
```http
POST /parse/url
Content-Type: application/json

{
  "url": "https://example.com/document.pdf"
}
```

### Upload and Parse
```http
POST /parse/upload
Content-Type: multipart/form-data

file: <your-file>
```

### Health Check
```http
GET /health
```

### API Documentation
- Interactive docs: `http://localhost:8080/docs`
- OpenAPI schema: `http://localhost:8080/openapi.json`

## Response Format

```json
{
  "success": true,
  "filename": "document.pdf",
  "file_type": ".pdf",
  "content_length": 1234,
  "content": "Extracted text content..."
}
```

## Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the development server
python main.py
```

### Development with Docker

```bash
# Build and run with volume mounting for live reload
docker-compose up --build
```

The volume mount in `docker-compose.yml` allows for live code reloading during development.

## Configuration

### Environment Variables

- `PYTHONPATH`: Set to `/app` (configured in Dockerfile)
- `PYTHONDONTWRITEBYTECODE`: Prevents Python from writing .pyc files
- `PYTHONUNBUFFERED`: Ensures output is sent straight to terminal

### File Upload Limits

- Default: 100MB (configured in Nginx)
- Timeout: 300 seconds for large file processing

## Docker Image Details

- **Base Image**: `python:3.11-slim`
- **Security**: Runs as non-root user
- **Health Checks**: Built-in health monitoring
- **Size Optimization**: Multi-stage build with `.dockerignore`

## Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   docker-compose down
   # Or change port in docker-compose.yml
   ```

2. **Permission denied**:
   ```bash
   sudo docker-compose up
   ```

3. **Build failures**:
   ```bash
   docker-compose build --no-cache
   ```

### Logs

```bash
# View API logs
docker-compose logs doc-parser-api

# Follow logs in real-time
docker-compose logs -f
```

## License

[Your License Here]

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with Docker
5. Submit a pull request 