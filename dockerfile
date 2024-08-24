# Use an official Python runtime as a parent image
FROM python:3.9-slim AS builder

# Set a working directory
WORKDIR /usr/src/app

# Install dependencies in a virtual environment for cleaner dependency management
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy the current directory contents into the container
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the rest of your app's source code and credentials
COPY ./app ./app

# Final stage
FROM python:3.9-slim AS runner
WORKDIR /usr/src/app
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /usr/src/app/app ./app

# Make sure scripts in the virtual env are used
ENV PATH="/opt/venv/bin:$PATH"

# Set the environment variable for Google credentials
ENV GOOGLE_APPLICATION_CREDENTIALS="/usr/src/app/app/credentials/neemble-eat-db-c49af78976aa.json"

# Non-root user for better security
RUN useradd -m myuser
USER myuser

# Make port 8000 available
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
