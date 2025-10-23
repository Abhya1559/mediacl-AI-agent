# 1. Use an official Python runtime as a parent image
FROM python:3.12.3-slim-bookworm

# 2. Set the working directory
WORKDIR /app

# 3. Copy *only* the requirements file first
# This lets us cache the installed packages
COPY requirements.txt .

# 4. Install the packages
# It will use the cache unless requirements.txt changes
RUN pip install --no-cache-dir -r requirements.txt

# 5. Now, copy the rest of your application code
COPY . .

# 6. Define the command to run your application
CMD ["python3", "app.py"]