# Cloud Run Dockerfile for Digsbody
FROM python:3.11-slim

WORKDIR /app

# Copy only what's needed
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy only the digsbody module and its dependencies
COPY daedalus/ ./daedalus/

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=10s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/api/digsbody/stats')" || exit 1

# Run the Digsbody API
CMD ["python", "-m", "uvicorn", "daedalus.digsbody.router:app", "--host", "0.0.0.0", "--port", "8080"]