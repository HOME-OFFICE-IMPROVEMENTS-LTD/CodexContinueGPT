# app/brain/planner.py

"""
CodexContinueGPT Planner - Converts objectives into step plans.
"""

class Planner:
    def __init__(self):
        self.objective = None

    def set_objective(self, text: str):
        self.objective = text

    def get_steps(self):
        # Temporary stub — replace with actual LLM-driven planning
        return [
            "Step 1: Understand the user query",
            "Step 2: Retrieve relevant memory or context",
            "Step 3: Respond or execute task"
        ]
