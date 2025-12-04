# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Make port 8001 available to the world outside this container
EXPOSE 8001

# Define environment variable
# ENV COMPANIES_HOUSE_API_KEY=... (Best passed via docker-compose or run command)

# Run bank_onboarding_mcp_server.py when the container# Run the application
CMD ["python", "companies_house_mcp.py"]
