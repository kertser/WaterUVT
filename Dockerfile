# Use the official Python image as the base image
FROM python:3.10.0

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY . /app

# Install the application dependencies
RUN pip install -r requirements.txt

# Define the entry point for the container
# CMD ["web: gunicorn -w 3 -k uvicorn.workers.UvicornWorker main:app"]
CMD ["gunicorn"  , "-w 3 -k", "0.0.0.0:8000", "main:app"]
