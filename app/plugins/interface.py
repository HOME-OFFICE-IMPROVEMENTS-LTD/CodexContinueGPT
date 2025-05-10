from abc import ABC, abstractmethod

class PluginInterface(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def execute(self, data):
        pass

    @abstractmethod
    def shutdown(self):
        pass

# CodexTool inherits the PluginInterface and adds a `name` + `description` + optional `run`
class CodexTool(PluginInterface):
    name: str
    description: str

    def run(self, input_text: str) -> dict:
        return self.execute(input_text)
