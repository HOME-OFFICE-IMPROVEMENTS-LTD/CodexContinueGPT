FROM python:3.11-slim

# Set working directory
WORKDIR /app

# System dependencies for development
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    build-essential \
    python3-dev \
    libffi-dev \
    libpq-dev \
    libssl-dev \
    curl \
    git \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user for development
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python development tools
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir pytest pytest-cov black flake8 isort mypy

# Copy requirements.txt and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create a marker file to prove this Dev Container Dockerfile is used
RUN echo "This container was built using the Dev Container Dockerfile" > /app/devcontainer-source.txt

# Expose the FastAPI default port
EXPOSE 8000

# Set the default user
USER $USERNAME

# We don't need a CMD here as devcontainer.json will handle that