# CodexContinue Backend API and Plugin Integration Guide

## Overview

This guide outlines how to integrate plugins into the CodexContinue backend architecture, with a focus on enabling seamless execution of plugins via API endpoints.

### Key Components
1. **PluginManager**: Responsible for loading, listing, and executing plugins dynamically.
2. **API Endpoints**: Interface for frontend to initiate plugin actions.
3. **Docker Integration**: Container-based plugin execution (Added: 2025-05-09)

### Plugin Integration Steps
1. **Define Your Plugin**: Ensure the plugin implements the `PluginInterface`.
2. **Load Plugins**: Use the `PluginManager` to dynamically load plugins from the `plugins` directory.
3. **API Endpoint Design**: Implement API endpoints that:
   - List available plugins.
   - Accept a plugin choice and input data.
   - Execute the selected plugin and return results.

### Docker-based Plugin Execution (Added: 2025-05-09)
When running in a Docker environment, plugins are executed within the backend container:

1. **Development Mode**: 
   - Plugins can be hot-reloaded when changed
   - Code is mounted from the host, so changes are reflected immediately
   - Use `./scripts/switch_env.sh dev` to enable development mode
   - Plugin changes are immediately detected without container restart

2. **Production Mode**:
   - Plugins are containerized with the application
   - Changes require rebuilding the container
   - Use `./scripts/switch_env.sh prod` for production deployment
   - Better performance and security for deployed environments

### Docker Configuration for Plugin Developers

#### Container Setup
- Backend plugins run in the backend container with access to:
  - Redis (for memory persistence)
  - Ollama (for local LLM inference)
  - Database (for plugin storage needs)

#### Environment Variables
Plugins have access to these environment variables:
```
PYTHONPATH=/app
ENV=development|production
REDIS_URL=redis://redis:6379
SQLITE_DB_PATH=/app/app/db/chat_memory.db
OLLAMA_BASE_URL=http://ollama:11434
```

#### Developing New Plugins in Docker
1. Create your plugin in the `/app/plugins` directory
2. Add your plugin dependencies to `/requirements.txt`
3. Use the VS Code tasks or run:
   ```bash
   # Restart backend to load new dependencies
   docker-compose restart backend
   
   # View logs to debug plugin behavior
   docker-compose logs -f backend
   ```

#### Docker Commands for Plugin Testing
```bash
# Test a specific plugin
docker-compose exec backend python -m app.scripts.run_plugin <plugin_name> "<input_data>"

# List available plugins
docker-compose exec backend python -m app.plugins.plugin_manager list
```

### Best Practices for Containerized Plugins

1. **Isolation & Security**:
   - Plugins should not access host filesystem directly
   - Store sensitive data in environment variables, not code
   - Use proper error handling for all operations

2. **Performance & Resource Management**:
   - Implement proper cleanup in the `shutdown()` method
   - Avoid high memory operations without pagination
   - Use connection pooling for external service connections
   - Configure appropriate timeouts for all plugin operations

3. **Cloud Deployment Readiness**:
   - For Azure deployments, ensure plugins support Managed Identity
   - Implement retry logic with exponential backoff for API calls
   - Add proper logging for monitoring and troubleshooting
   - Handle transient failures gracefully

### Example API Workflow

#### 1. List Available Plugins
- Method: `GET /api/plugins`
- Description: Returns a list of available plugins.

#### 2. Execute Plugin
- Method: `POST /api/plugins/execute`
- Request Body:
  ```json
  {
      "plugin": "plugin_name",
      "data": "input_data"
  }
  ```
- Description: Executes the specified plugin with input data and returns the result.

---

### Plugin Naming Convention

- File must be named like: `example_plugin.py`
- Class inside must be named: `ExamplePlugin` (PascalCase of file)
- Must implement `PluginInterface`

Example:

```python
class MyPlugin(PluginInterface):
    ...

## 🧩 Plugin System (Updated 2025-05-03)

CodexContinueGPT supports dynamic plugin loading. Plugins must follow the `PluginInterface` located at `app/plugins/interface.py`.

### Plugin Requirements
- Must end in `_plugin.py`
- Must implement:
  - `initialize()`
  - `execute(data)`
  - `shutdown()`

### Example

```python
from app.plugins.interface import PluginInterface

class MyPlugin(PluginInterface):
    def initialize(self): ...
    def execute(self, data): ...
    def shutdown(self): ...

Plugins are auto-loaded via PluginManager and are executable by name.    

"""
🚀 Milestone Recorded — 2025-05-03
- PluginManager verified with dynamic plugin discovery.
- `huggingface_plugin` and `calculator_plugin` conform to interface.
- OpenInterpreter alias + testing alias added.
- PluginRegistry tested and functional.
- Documentation updated in Plugin_API_Integration_Guide.md
"""
### 🧠 Milestone Recorded — 2025-05-04

- Plugin Runner system (`scripts/run_plugin.py`) is complete and verified.
- Shell, Memory, and Agent plugins are now fully compatible with CodexTool.
- Full plugin registry (`register_all_plugins`) allows modular plugin control.
- All CLI runners and test cases pass, with memory and command execution plugins responding.
- Plugin API documentation and developer guides are updated accordingly.
- Project now supports `/run <plugin> <input>` style shell interfacing.

Next:
- Refactor `/chat` endpoint to support tool-based dispatch.
- Introduce Plugin Agent as a conversational middleware layer.
###

## 🔌 Plugin Agent Dispatch

CodexContinueGPT supports direct plugin invocation inside chat sessions.

### Usage

Send messages in the format: 
/run <plugin_name> <input_data>

### Example/run shell echo hello
/run shell echo hello

This bypasses LLM and invokes the registered plugin. The PluginAgent is used to intercept such commands.


### 🧠 Milestone Recorded — 2025-05-04 (Afternoon)

- Memory audit API `/memory/audit/{session_id}` introduced for developers.
- Supports frontend visualization or debugging of memory timeline.
- Example added: `curl http://localhost:8000/memory/audit/default`
- Route automatically registered in `main.py`.

## 🔌 Plugin Implementation Examples

### Basic Plugin Template

```python
from app.plugins.interface import PluginInterface

class MyCustomPlugin(PluginInterface):
    """
    Example plugin that demonstrates the basic implementation pattern.
    """
    
    def initialize(self):
        """Called when plugin is loaded"""
        self.name = "my_custom_plugin"
        self.description = "Example plugin for demonstration purposes"
        return True
        
    def execute(self, data):
        """Called when plugin is executed"""
        try:
            # Process input data
            result = f"Processed: {data}"
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}
            
    def shutdown(self):
        """Called when plugin is unloaded"""
        # Clean up resources
        return True
```

### Docker-Aware Plugin Example

```python
import os
import redis
from app.plugins.interface import PluginInterface

class DockerAwarePlugin(PluginInterface):
    """
    Example plugin that demonstrates Docker environment awareness.
    """
    
    def initialize(self):
        """Called when plugin is loaded"""
        self.name = "docker_aware_plugin"
        self.description = "Plugin that uses Docker environment variables"
        
        # Access environment variables from Docker
        self.env = os.environ.get("ENV", "development")
        self.redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
        
        # Connect to Redis if available
        try:
            self.redis = redis.from_url(self.redis_url)
            self.redis.ping()  # Test connection
            self.redis_available = True
        except Exception:
            self.redis_available = False
        
        return True
        
    def execute(self, data):
        """Called when plugin is executed"""
        result = {
            "env": self.env,
            "redis_available": self.redis_available,
            "input": data
        }
        
        # Store results in Redis if available
        if self.redis_available:
            try:
                key = f"plugin_result:{self.name}:{data}"
                self.redis.set(key, str(result))
                self.redis.expire(key, 3600)  # Expire after 1 hour
                result["stored_in_redis"] = True
            except Exception as e:
                result["redis_error"] = str(e)
        
        return result
            
    def shutdown(self):
        """Called when plugin is unloaded"""
        # Clean up Redis connection
        if hasattr(self, "redis") and self.redis_available:
            try:
                # Clean up any temporary keys if needed
                pass
            except Exception:
                pass
        return True
```

## 🔄 Docker Development Workflow for Plugins

### Local Development Loop

1. **Create Plugin**: Create your plugin file in `app/plugins/`
2. **Test Locally**: Run plugin locally with `python -m app.scripts.run_plugin`
3. **Deploy to Docker**: Use development mode for quick iteration

### Automated Testing in Docker

```bash
# Create a test script for your plugin
cat > tests/test_my_custom_plugin.py << 'EOF'
import pytest
from app.plugins.plugin_manager import PluginManager

def test_my_custom_plugin():
    manager = PluginManager()
    manager.load_plugins()
    
    # Test plugin loading
    assert "my_custom_plugin" in manager.get_plugin_list()
    
    # Test plugin execution
    result = manager.execute_plugin("my_custom_plugin", "test input")
    assert result["status"] == "success"
EOF

# Run the test in Docker
docker-compose exec backend pytest tests/test_my_custom_plugin.py -v
```

## 🚀 Deploying Plugins to Production

### Pre-Deployment Checklist

- [ ] Plugin follows naming convention (`*_plugin.py`)
- [ ] Plugin implements all required methods
- [ ] Plugin passes all tests in development environment
- [ ] Plugin dependencies are added to `requirements.txt`
- [ ] Plugin respects resource constraints
- [ ] Plugin handles errors gracefully

### Production Deployment Steps

1. Add your plugin to the codebase
2. Update `requirements.txt` with any dependencies
3. Switch to production mode: `./scripts/switch_env.sh prod`
4. Build and deploy: `docker-compose build && docker-compose up -d`
5. Verify plugin functionality: `docker-compose exec backend python -m app.scripts.run_plugin <plugin_name> "test"`

### Monitoring Plugin Execution

Access logs for plugin execution in production:

```bash
docker-compose logs -f backend | grep "PluginManager"
```

## 📊 Plugin Performance Considerations

- **Memory Usage**: Monitor memory consumption, especially with LLM-based plugins
- **Execution Time**: Keep response times under 5 seconds for interactive plugins
- **External Dependencies**: Cache results where appropriate
- **Error Rates**: Track and minimize error rates in plugin execution

---
