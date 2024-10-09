# Use a base Python image
FROM python:3.9-slim
# Set the working directory in the container
WORKDIR /app
# Copy the requirements file to the container
COPY requirements.txt .
# Install dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Copy the current directory contents into the container at /app
COPY . /app
# Install dependencies, including FastAPI, asyncpg, httpx, and curl
RUN apt-get update && apt-get install -y curl \
    && pip install fastapi uvicorn asyncpg httpx
# Expose the port FastAPI runs on
EXPOSE 9000
# Run FastAPI
CMD ["uvicorn", "healthcheck_service:app", "--host", "0.0.0.0", "--port", "9000"]