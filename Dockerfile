# ---------- Builder stage ----------
FROM python:3.12-slim AS builder

WORKDIR /app

# Install build dependencies only if needed (kept minimal)
RUN apt-get update && apt-get install -y 

# Copy only requirements first for better layer caching
COPY requirements.txt .

# Create virtual environment and install deps
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# ---------- Runtime stage ----------
FROM python:3.12-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv

# Copy application code (after deps to maximize caching)
COPY . .

# Change ownership
RUN chown -R appuser:appuser /app

USER appuser

EXPOSE 5000

CMD ["python", "app.py"]
