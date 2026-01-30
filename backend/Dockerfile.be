# Start with a small Python base to keep things light
FROM python:3.14-slim AS builder

# Prevent Python from writing .pyc files and keep logs coming in real-time
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /build

# Need these to compile some Python packages (like cryptography for your ES256)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install everything to a specific prefix so we can just grab it later
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Moving to the clean runtime image
FROM python:3.14-slim AS runtime

WORKDIR /app

# Required for 'python-magic' to validate those ZIP uploads
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Grab the pre-installed packages from the builder stage
COPY --from=builder /install /usr/local

# Pull in the rest of the backend source code
COPY . .

# Ensure the folder for your ES256 .pem files exists
RUN mkdir -p certs

# Pull the port from the build args or fallback to 8080
ARG APP_PORT=8080
EXPOSE ${APP_PORT}

# Fire up the API. Shell form allows $APP_PORT to be picked up from the env.
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${APP_PORT}"]
