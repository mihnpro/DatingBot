FROM python:3.11-slim

WORKDIR /app

# Установка uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Системные зависимости (curl для healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Копирование файлов зависимостей
COPY pyproject.toml uv.lock ./

# Установка зависимостей в виртуальное окружение
RUN uv sync --no-dev --no-install-project

# Копирование исходного кода
COPY src/ ./src/

# Открываем порт
EXPOSE 8000

# Запуск через uv run (активирует виртуальное окружение)
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]