# Use lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy MCP server code
COPY . .

# Expose MCP server port
EXPOSE 9002

# Run MCP server (replace server:app with your FastAPI MCP app)
CMD ["uvicorn", "mcp-server:app", "--host", "0.0.0.0", "--port", "9002"]
