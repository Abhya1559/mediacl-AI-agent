# 1. Use an official Python runtime as a parent image
FROM python:3.12.3-slim-bookworm

# 2. Set the working directory
WORKDIR /app

# 3. Install system dependencies
# This is needed to compile packages like sentence-transformers, numpy, etc.
# We do this before pip install
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 4. Copy *only* the requirements file first
# This lets us cache the installed packages
COPY requirements.txt .

# 5. Install the python packages
# It will use the cache unless requirements.txt changes
RUN pip install --no-cache-dir -r requirements.txt

# 6. Now, copy the rest of your application code
COPY . .

# 7. Define the command to run your application
CMD ["python3", "app.py"]

