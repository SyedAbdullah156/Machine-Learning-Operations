# Base Python Image
From python:3.11-slim
# Create directory for cache purposes
COPY . /app
# Set Current Working Directory
WORKDIR /app
# Install dependencies
RUN pip install -r requirements
# Command to run app.py file
CMD python app.py
