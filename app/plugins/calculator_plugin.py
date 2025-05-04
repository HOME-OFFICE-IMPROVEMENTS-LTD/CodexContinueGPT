# app/plugins/calculator_plugin.py

from app.plugins.interface import PluginInterface

class CalculatorPlugin(PluginInterface):
    def initialize(self):
        print("Calculator Plugin initialized.")

    def execute(self, data):
        try:
            result = eval(data, {"__builtins__": {}}, {})
            return {"result": result}
        except Exception as e:
            return {"error": str(e)}

    def shutdown(self):
        print("Calculator Plugin shutting down.")
