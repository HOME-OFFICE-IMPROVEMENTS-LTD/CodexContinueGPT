# tests/test_plugin_manager.py

from app.plugins.manager import PluginManager

def test_huggingface_plugin_execution():
    manager = PluginManager()
    assert 'huggingface_plugin' in manager.list_plugins()

    result = manager.execute_plugin('huggingface_plugin', "I love CodexContinue!")
    assert isinstance(result, list)
    assert 'label' in result[0]
    assert 'score' in result[0]

