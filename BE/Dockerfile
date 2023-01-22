FROM python:3.10-alpine

# Install Poetry
RUN python -m pip install poetry

# Set working directory
WORKDIR /app

# Add volume for src directory
VOLUME /workspace/K-army-project/insta-character/BE:/app

# Install dependencies
RUN poetry install

WORKDIR src

CMD ["poetry", "run", "uvicorn", "main:app", "--reload", "--port", "8000", "--host", "0.0.0.0"]