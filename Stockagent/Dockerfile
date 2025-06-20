# Use official slim Python base image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy code and dependencies
COPY stock_agent.py /app/
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for FastMCP (same as PORT)
EXPOSE 8000

# Default command to run the MCP server
CMD ["python", "stock_agent.py"]
