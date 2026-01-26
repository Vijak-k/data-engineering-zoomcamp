# Use a slim Python image to keep the final container size small
FROM python:3.13.11-slim

# Copy the 'uv' binary from the official Astral image for fast dependency management
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

# Set the working directory inside the container
WORKDIR /code

# Ensure the virtual environment created by uv is automatically used by Python
ENV PATH="/code/.venv/bin:$PATH"

# Copy dependency files first to leverage Docker's layer caching
# Changes to your code won't trigger a full re-install of packages
COPY pyproject.toml .python-version uv.lock ./

# Install dependencies exactly as specified in the lockfile
RUN uv sync --locked

# Copy the application script into the container
COPY ingest_data.py .

# Define the command to run when the container starts
ENTRYPOINT ["python", "ingest_data.py"]