FROM python:3.11-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements .
RUN pip install --no-cache-dir -r requirements

COPY . .

EXPOSE 5000

# For development/demo we run Flask directly.
CMD ["python", "app.py"]
