# StreamlitDuplicateElementKey Fix

## Error Description

The application was experiencing the following error when the backend service was unreachable:

```
streamlit.errors.StreamlitDuplicateElementKey: There are multiple elements with the same key='retry_connection_http___localhost_8000_models'. To fix this, please make sure that the key argument is unique for each element you create.
```

## Issue Cause

The error occurred because multiple connection errors triggered the `show_connection_error()` function, which created multiple buttons with the same key. Specifically:

1. When the backend was unreachable, multiple API calls would fail
2. Each failure would call `show_connection_error(url)`
3. Each call would create a "Retry Connection" button with a key derived from the URL
4. When the same endpoint was called multiple times (e.g., for models, status), identical keys were generated
5. Streamlit requires all element keys to be unique within a session

## Fix Implemented

The fix adds a session-based counter to ensure each button key is unique:

```python
def show_connection_error(url):
    """Display formatted connection error with troubleshooting tips"""
    # Create a unique identifier for this error instance
    if "connection_error_counter" not in st.session_state:
        st.session_state.connection_error_counter = 0
    st.session_state.connection_error_counter += 1
    
    # ... rest of function ...
    
    # Using a unique key with counter for each retry button
    unique_key = f"retry_connection_{url.replace(':', '_').replace('/', '_')}_{st.session_state.connection_error_counter}"
    if st.button("Retry Connection", key=unique_key):
        # ... button functionality ...
```

## Best Practices for Streamlit Keys

When working with Streamlit elements that require keys:

1. Always ensure keys are unique for each element
2. For dynamically generated elements, incorporate a counter or timestamp
3. When elements might be regenerated (like in error handlers), use session state to track counters
4. Avoid using only URL paths as keys since the same endpoint might be called multiple times
5. Consider adding the function name or call site information to keys for better traceability

## Related Files

- `/frontend/app.py` - Contains the `show_connection_error()` function that was updated

## Testing

After implementing this fix:
1. The application no longer crashes with duplicate key errors when the backend is unavailable
2. Multiple connection error messages can be displayed without conflicts
3. Each "Retry Connection" button functions independently
