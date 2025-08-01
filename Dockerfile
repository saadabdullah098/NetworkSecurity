FROM python:3.10-slim-buster

# Set working directory
WORKDIR /app

# Copy app code into the container working directory
COPY . /app

# Install awscli without extra dependencies and clean up apt cache
RUN apt update && \
    apt install -y --no-install-recommends awscli && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies without caching to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run your app
CMD ["python3", "app.py"]
