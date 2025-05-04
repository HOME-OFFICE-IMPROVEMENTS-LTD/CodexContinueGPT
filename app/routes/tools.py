# app/routes/tools.py

from fastapi import APIRouter
from app.plugins.register_all import register_all_plugins

router = APIRouter()
registry = register_all_plugins()

@router.get("/tools")
def list_tools():
    return {
        "tools": [
            {
                "name": tool.name,
                "description": tool.description
            }
            for tool in registry.all().values()
        ]
    }
