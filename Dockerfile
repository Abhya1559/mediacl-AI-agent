FROM python:3.12.3-slim-bookworm

# 2. Set the working directory in the container to /app
WORKDIR /app

# 3. Copy the current directory contents into the container at /app
# This includes your app.py and requirements.txt
COPY . /app

# 4. Install any needed packages specified in requirements.txt
# Using --no-cache-dir reduces the final image size
RUN pip install --no-cache-dir -r requirements.txt

# 5. Define the command to run your application
# This will run "python3 app.py" when the container launches
CMD ["python3", "app.py"]