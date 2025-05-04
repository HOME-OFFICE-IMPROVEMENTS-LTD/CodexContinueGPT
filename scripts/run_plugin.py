# scripts/run_plugin.py

import sys
from app.plugins.register_all import register_all_plugins

if len(sys.argv) < 3:
    print("Usage: python scripts/run_plugin.py <plugin_name> <input>")
    sys.exit(1)

plugin_name = sys.argv[1]
input_text = " ".join(sys.argv[2:])

registry = register_all_plugins()
plugin = registry.get(plugin_name)

if plugin:
    plugin.initialize()
    result = plugin.run(input_text)
    plugin.shutdown()
    print(result)
else:
    print(f"Plugin '{plugin_name}' not found.")
