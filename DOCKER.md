# Docker Configuration Guide

This project supports both development containers (Dev Containers) and production Docker configurations.

## Development Environment

### Option 1: Using VS Code Dev Containers

1. Install the [Dev Containers extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) for VS Code
2. Open the project folder in VS Code
3. When prompted, click "Reopen in Container" or run the command "Dev Containers: Reopen in Container"
4. VS Code will build the development container and set up the environment automatically

### Option 2: Using Docker Compose with Development Configuration

```bash
# Copy the development environment file
cp .env.development .env

# Build and run the development environment
docker-compose build
docker-compose up -d
```

## Production Environment

For production deployments:

```bash
# Copy the production environment file
cp .env.production .env

# Build and run the production environment
docker-compose build
docker-compose up -d
```

## Configuration Files

- **Main Dockerfile**: Used for production deployments
- **.devcontainer/Dockerfile**: Used for development with VS Code Dev Containers
- **.devcontainer/devcontainer.json**: Dev Container configuration
- **docker-compose.yml**: Orchestrates all services (backend, frontend, redis, ollama)
- **.env.development**: Environment variables for development
- **.env.production**: Environment variables for production

## Key Differences

| Feature | Development | Production |
|---------|-------------|------------|
| Python Version | 3.11 | 3.11 |
| Code Mounting | Mounted for hot reload | Containerized code |
| Dev Tools | Includes testing, linting | Minimal dependencies |
| User | vscode user (non-root) | Default (root) |
| Reload | Enabled | Disabled |

## Environment Variables

Environment variables can be customized in the `.env` file or through `.env.development` and `.env.production`.

### Important Environment Variables

| Variable | Purpose | Default Value |
|----------|---------|---------------|
| ENV | Sets environment mode | development/production |
| DOCKERFILE_PATH | Specifies Dockerfile to use | .devcontainer/Dockerfile or Dockerfile |
| MOUNT_CODE | Controls code mounting for hot reload | .:/app or empty |
| RELOAD | Controls Uvicorn hot reload | --reload or empty |
| PYTHONPATH | Sets Python module search path | /app |

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError: No module named 'app'**
   - Make sure PYTHONPATH is set to `/app` in your environment
   - In the command section of docker-compose.yml, explicitly set PYTHONPATH for commands

2. **ModuleNotFoundError for dependencies**
   - Ensure requirements.txt is properly copied and installed in .devcontainer/Dockerfile
   - Check for any missing dependencies with `pip freeze > requirements.txt`

3. **Container build issues**
   - Use `docker-compose build --no-cache` to rebuild without cache
   - Check logs with `docker-compose logs [service_name]`

4. **API Connection Errors**
   - If the frontend can't connect to the backend, check that:
     - Both containers are running: `docker-compose ps`
     - Backend container logs don't show startup errors: `docker-compose logs backend`
     - Environment variables BACKEND_HOST and BACKEND_PORT are set correctly in .env
     - Try accessing the backend directly: `curl http://localhost:8000/health`
     - In Docker environments, frontend should use `backend` as the host, not `localhost`

5. **Service Discovery Issues**
   - Ensure all containers are on the same network: `docker network inspect codexcontinuegpt_codexnet`
   - Try restarting just the problematic container: `docker-compose restart [service_name]`
   - If network issues persist, try recreating the network: `docker-compose down && docker-compose up -d`

6. **Data Persistence Issues**
   - Check Redis connection: `docker-compose exec redis redis-cli ping` (should return PONG)
   - Verify database file exists: `docker-compose exec backend ls -la /app/app/db/chat_memory.db`
   - If database is corrupted, you can reset it: `docker-compose exec backend python app/db/init_db.py`
