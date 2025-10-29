# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy the requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY agent.py .

# Expose the port your ADK web application listens on (e.g., 8000)
EXPOSE 8000

# Change to /usr/src before running the command
WORKDIR /usr/src

# Set the command to run the ADK web application
# Ensure to bind to 0.0.0.0 for external access within the container
CMD ["adk", "web", "--host", "0.0.0.0", "--port", "8000"]