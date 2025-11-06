# ocr-service

[RU 🇷🇺](README.md) | [EN 🇬🇧](README.en.md)

FastAPI service for extracting text from images using Pytesseract. RabbitMQ serves as the Celery broker, while Redis is used as the Celery backend and cache.

## Quick start

1. **Clone the repository:**
    ```bash
    git clone https://github.com/EXsiDe4299/ocr-service.git
    ```
   
2. **Go to the project directory:**
    ```bash
    cd ocr-service
    ```
   
3. **Configure the environment:**

    Create a `.env` file and configure the environment variables.

    - Linux:
    ```bash
    cp .env.template .env
    ```
   
    - Windows:
    ```bash
    copy .env.template .env
    ```
   
4. **Run Docker Compose:**
    ```bash
    docker compose up -d
    ```

5. **Try the app:**

    Open http://0.0.0.0:8000/docs to view Swagger documentation. RabbitMQ Management will be available at http://0.0.0.0:15672

## Features

- **OCR** – Extracts text from images using Pytesseract.
- **Background Tasks** – Processes images in Celery with a RabbitMQ broker and Redis backend.
- **Caching** – Prevents re‑processing of the same images by leveraging Redis.
- **Task Status Management** – Marks published tasks as ACCEPTED to track their state.