FROM python:3.13-slim AS builder
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential git git-lfs \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copy dependency files first 
COPY mlapi/pyproject.toml mlapi/poetry.lock ./

# Create venv
RUN python -m venv ./venv
ENV PATH="/app/venv/bin:$PATH"

# Disable Poetry's own venv creation
RUN poetry config virtualenvs.create false

# Install dependencies into this new venv
RUN /bin/bash -c "source ./venv/bin/activate && poetry install --only main --no-root"

# Copy source code (from mlapi/src/)
COPY mlapi/src ./src

# Copy the model into the builder stage
COPY distilbert-base-uncased-finetuned-sst2 ./distilbert-base-uncased-finetuned-sst2

FROM python:3.13-slim AS runtime
WORKDIR /app

# Copy venv, model and source code from builder
COPY --from=builder /app/venv ./venv
COPY --from=builder /app/src ./src
COPY --from=builder /app/distilbert-base-uncased-finetuned-sst2 ./distilbert-base-uncased-finetuned-sst2

# Add venv to PATH
ENV PATH="/app/venv/bin:$PATH"

# Expose port
EXPOSE 8000

# Start the FastAPI app with uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]