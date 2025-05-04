
# app/plugins/huggingface_plugin.py

from transformers import pipeline
from app.plugins.interface import PluginInterface

class HuggingfacePlugin(PluginInterface):
    def __init__(self):
        self.model = None

    def initialize(self):
        self.model = pipeline('sentiment-analysis')
        print("[HuggingfacePlugin] Model loaded")

    def execute(self, data):
        if not self.model:
            raise RuntimeError("Model not initialized.")
        # Expecting data to be a string or list of strings
        return self.model(data)

    def shutdown(self):
        self.model = None
        print("[HuggingfacePlugin] Resources cleaned up")
