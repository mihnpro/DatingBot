FROM python:3.11

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install UV
RUN pip install uv

# Copy dependency files
COPY pyproject.toml uv.lock* README.md ./

# Copy the entire application
COPY . .

# Create a simple setup.py for compatibility (optional)
RUN echo "from setuptools import setup, find_packages; setup(name='user-service', packages=find_packages())" > setup.py

# Install dependencies
RUN uv venv /opt/venv && \
    . /opt/venv/bin/activate && \
    uv pip install -e .

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app /opt/venv
USER appuser

# Set environment variables
ENV PATH="/opt/venv/bin:${PATH}"
ENV PYTHONPATH="/app:${PYTHONPATH}"

# Run application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]