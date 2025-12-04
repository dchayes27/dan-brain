# Use a slim Python image to keep size down
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install system dependencies (gcc is often needed for python libs)
RUN apt-get update && apt-get install -y build-essential

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy our brain code
COPY agent_master.py .

# Expose port 8000
EXPOSE 8000

# Run the brain
CMD ["python", "agent_master.py"]
