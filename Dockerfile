
FROM python:3.12


ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app


RUN apt-get update && apt-get install -y --no-install-recommends \
build-essential 


COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY . .




CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]
