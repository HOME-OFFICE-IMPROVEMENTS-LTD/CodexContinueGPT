# app/plugins/agent_plugin.py

class AgentPlugin:
    def __init__(self):
        pass

    def initialize(self):
        print("Agent plugin initialized")

    def execute(self, data: str):
        return {"agent_response": f"🧠 Agent plugin processed: {data}"}

    def run(self, data: str):
        return self.execute(data)

    def shutdown(self):
        print("Agent plugin shutdown")

    def handle(self, message: str, session_id: str) -> str:
        # 🧠 Default fallback behavior
        return f"🧠 (default agent) I received: '{message}'"
