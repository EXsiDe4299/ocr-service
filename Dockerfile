FROM python:3.12.3-bookworm

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV PYTHONBUFFERED=1

ENV UV_NO_DEV=1

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends tesseract-ocr tesseract-ocr-rus tesseract-ocr-eng \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./pyproject.toml

RUN uv sync

COPY . /app

CMD ["uv", "run", "main.py"]