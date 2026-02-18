# syntax=docker/dockerfile:1

FROM python:3.11-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

# Install yep from source (PEP 517 build via pyproject.toml)
COPY pyproject.toml README.md LICENSE /app/
COPY src /app/src

RUN pip install --no-cache-dir .

ENTRYPOINT ["yep"]
CMD ["--help"]
