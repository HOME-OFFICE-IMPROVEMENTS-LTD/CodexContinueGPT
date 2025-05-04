
# CodexContinue Backend API and Plugin Integration Guide

## Overview

This guide outlines how to integrate plugins into the CodexContinue backend architecture, with a focus on enabling seamless execution of plugins via API endpoints.

### Key Components
1. **PluginManager**: Responsible for loading, listing, and executing plugins dynamically.
2. **API Endpoints**: Interface for frontend to initiate plugin actions.

### Plugin Integration Steps
1. **Define Your Plugin**: Ensure the plugin implements the `PluginInterface`.
2. **Load Plugins**: Use the `PluginManager` to dynamically load plugins from the `plugins` directory.
3. **API Endpoint Design**: Implement API endpoints that:
   - List available plugins.
   - Accept a plugin choice and input data.
   - Execute the selected plugin and return results.

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
