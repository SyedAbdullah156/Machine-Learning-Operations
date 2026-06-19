# File: mlflow_server/Dockerfile
FROM python:3.10

WORKDIR /mlflow

# Install MLflow and dependencies
RUN pip install mlflow==2.14 psycopg2-binary boto3

# Expose port 5000 (MLflow UI)
EXPOSE 5000

# Copy entrypoint script
COPY entrypoint.sh .

# Make script executable
RUN chmod +x entrypoint.sh

# Default command
CMD ["./entrypoint.sh"] 