# app/routes/plugin_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.plugins.register_all import register_all_plugins

router = APIRouter()
registry = register_all_plugins()

class PluginRunRequest(BaseModel):
    plugin: str
    data: str

@router.get("/plugins")
def list_plugins():
    return {"plugins": list(registry.all().keys())}

@router.post("/plugins/execute")
def run_plugin(request: PluginRunRequest):
    try:
        plugin = registry.get(request.plugin)
        if not plugin:
            raise HTTPException(status_code=404, detail="Plugin not found")

        plugin.initialize()
        result = plugin.run(request.data)
        plugin.shutdown()
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
