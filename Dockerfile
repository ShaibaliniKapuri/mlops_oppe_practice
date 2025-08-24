# 1. Use an official Python runtime as a parent image
# We start with a slim, lightweight version of Python 3.10 to keep our final image size small.
FROM python:3.10-slim

# 2. Set the working directory inside the container
# This command sets the default directory for all subsequent commands.
# It's where our application code will live.
WORKDIR /app

# 3. Copy files from your local machine to the container
# The first '.' refers to the current directory on your local machine (where the Dockerfile is).
# The '/app' is the destination directory inside the container (which we set with WORKDIR).
# This copies main.py, requirements.txt, etc., into the container.
COPY . /app

# 4. Install the Python dependencies
# This runs the pip installer to download and install the packages listed in requirements.txt.
# --no-cache-dir is a good practice for Docker as it reduces the image size by not storing the cache.
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose a port on the container
# This informs Docker that the container listens on port 8200 at runtime.
# It doesn't actually publish the port; it's more like documentation.
EXPOSE 8100

# 6. Command to run the server when the container starts
# This is the command that will be executed when the container launches.
# It starts the Uvicorn server to run our FastAPI application.
# "iris_fastapi:app" means "in the file iris_fastapi.py, run the object named app".
# --host "0.0.0.0" makes the server accessible from outside the container.
CMD ["uvicorn", "serve:app", "--host", "0.0.0.0", "--port", "8200"]
