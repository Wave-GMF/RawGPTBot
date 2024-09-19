FROM python:3.9-alpine

LABEL org.opencontainers.image.authors="Maksim Alekseev <maksimgoody@gmail.com>"

ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on

WORKDIR /app

COPY requirements.txt .

RUN apk --no-cache add ffmpeg \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["python", "bot/main.py"]
