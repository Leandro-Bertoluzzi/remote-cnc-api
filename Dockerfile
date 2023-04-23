# Use the latest Ubuntu image as the base image
FROM ubuntu:latest

# Update the package list and install the required packages
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    make

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required packages from requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy the Flask application into the container
COPY . .

# Start the Flask application
CMD [ "flask", "run", "--host=0.0.0.0" ]
