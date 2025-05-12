# Streamlit Best Practices for CodexContinueGPT

This document outlines best practices for working with Streamlit in the CodexContinueGPT project to avoid common errors and ensure consistent implementation.

## Page Configuration

### The `st.set_page_config()` Rule

```python
import streamlit as st

# MUST be the first Streamlit command after imports
st.set_page_config(
    page_title="Page Title",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Now you can import other libraries
import pandas as pd
import other_libraries
```

**Important Rules:**
- `st.set_page_config()` must be called **only once** per Streamlit page
- It must be the **first Streamlit command** in your script
- Always place it immediately after importing streamlit, before any other imports that might use streamlit
- Document this requirement with a comment to prevent future developers from making the same mistake

### Common Errors to Avoid

1. **Multiple `set_page_config()` calls:**
   ```python
   # This will cause an error if both are in the same file
   st.set_page_config(...)  # Top of file
   # ...other code...
   st.set_page_config(...)  # Later in the file - WRONG!
   ```

2. **Importing modules that use Streamlit before `set_page_config()`:**
   ```python
   import streamlit as st
   from my_module import something  # If this module uses st.something(), it could cause an error
   
   st.set_page_config()  # Too late! - WRONG!
   ```

3. **Calling other Streamlit commands before `set_page_config()`:**
   ```python
   import streamlit as st
   
   st.title("My App")  # WRONG - st.title() before set_page_config()
   st.set_page_config()  # Too late!
   ```

## Project Structure for Streamlit Multi-page Apps

### Page Organization

- Main app: `frontend/app.py`
- Additional pages: `frontend/pages/N_PageName.py`
- Each page file should be completely self-contained
- Avoid importing functions that call Streamlit commands from other files

### Sharing Code Between Pages

For sharing code between pages without violating the `set_page_config()` rule:

1. **Create utility modules that don't use Streamlit:**
   ```python
   # utils.py - No Streamlit commands here
   def process_data(data):
       # Data processing logic
       return processed_data
   ```

2. **If you need to share Streamlit components, create factory functions:**
   ```python
   # components.py
   def create_metric_card(title, value):
       """Returns a function that will create a metric card.
       This avoids executing Streamlit commands at import time."""
       def _create_card():
           return st.markdown(f"""
               <div class="metric-card">
                   <div class="metric-value">{value}</div>
                   <div class="metric-title">{title}</div>
               </div>
           """, unsafe_allow_html=True)
       return _create_card
   ```

3. **Use conditional imports for shared configuration:**
   ```python
   # In your page file:
   try:
       # Import only variables, not Streamlit functions
       from app import CONFIG_VARIABLES
   except ImportError:
       # Fallback configuration
       CONFIG_VARIABLES = {"default": "value"}
   ```

## Testing Streamlit Pages

Before committing changes:

1. Test each page individually:
   ```bash
   streamlit run frontend/pages/1_PageName.py
   ```

2. Test the full app with all pages:
   ```bash
   streamlit run frontend/app.py
   ```

3. Check for console errors when navigating between pages

## Docker Considerations

When running Streamlit in Docker:

1. Make sure the container has access to all required Python modules
2. Use proper port mapping (`8501:8501`)
3. Set `--server.headless=true` for headless operation
4. For development mode, use volume mounts for code changes without rebuilding

## Troubleshooting Common Issues

### Page Config Error

If you see:
```
streamlit.errors.StreamlitSetPageConfigMustBeFirstCommandError
```

Check:
1. Is `st.set_page_config()` called more than once?
2. Is there any Streamlit command before `st.set_page_config()`?
3. Are you importing modules that use Streamlit before calling `st.set_page_config()`?

### Cache Issues

If changes aren't showing up:
1. Clear browser cache
2. Restart the Streamlit server
3. Use `?cache=false` in the URL
