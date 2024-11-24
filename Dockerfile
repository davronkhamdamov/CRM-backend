FROM python:3.9-slim

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/* \

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

# EXPOSE 8000

# CMD ["uvicorn", "app.app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
