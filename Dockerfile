FROM python:3.10-slim-bullseye

# Set working directory
WORKDIR /app

# Copy app code into the container
COPY . /app

# Install awscli and clean up apt cache
RUN apt-get update && \
    apt-get install -y --no-install-recommends awscli && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Default command to run your app
CMD ["python3", "app.py"]
