# Use an official Python runtime as a parent image
FROM python:3.12.7-slim AS builder

# Set a working directory
WORKDIR /usr/src/app

# Install dependencies in a virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy dependencies and install them
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application source code
COPY ./app ./app



# Final stage
FROM python:3.12.7-slim AS runner

WORKDIR /usr/src/app

# Copy the virtual environment and application code
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /usr/src/app/app ./app

# Copy .env
COPY .env .env

# Ensure virtual environment is used
ENV PATH="/opt/venv/bin:$PATH"

# Non-root user for better security
RUN useradd -m myuser

# Create uploads directory and set permissions
RUN mkdir -p /usr/src/app/app/uploads && \
    chown -R myuser:myuser /usr/src/app/app/uploads && \
    chmod -R 755 /usr/src/app/app/uploads

# Change to non-root user
USER myuser

# Expose the application port

ENV PORT 8000
ENV DOTENV_PATH="/usr/src/app/.env"


EXPOSE 8000

# Run the FastAPI app with Uvicorn
CMD exec uvicorn app.main:app --host 0.0.0.0 --port 8000
