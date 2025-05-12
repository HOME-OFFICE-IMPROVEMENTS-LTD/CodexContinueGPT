# Analytics Dashboard Fix

## Issue

The Analytics Dashboard page was failing to load with the following error:

```
streamlit.errors.StreamlitSetPageConfigMustBeFirstCommandError: set_page_config() can only be called once per app page, and must be called as the first Streamlit command in your script.
```

## Root Cause

The error was caused by having duplicate `st.set_page_config()` calls in the Analytics Dashboard page:

1. One at the top of the file (line 4-10)
2. Another after the imports and configuration section (around line 60-66)

In Streamlit, `set_page_config()` must only be called once per page and must be the first Streamlit command executed.

## Solution

We fixed the issue by:

1. Keeping only the first `st.set_page_config()` call at the top of the file
2. Removing the second duplicate call that was occurring later in the code
3. Ensuring no other Streamlit commands were executed before the `set_page_config()` call

## Affected Files

- `/frontend/pages/3_Analytics_Dashboard.py`
- `/frontend/pages/7_API_Keys.py` (previously fixed)
- `/frontend/pages/plugin_explorer.py` (newly discovered and fixed)

## Related Documentation

See also:
- `/docs/FIXES_Streamlit_and_API_Keys.md` - Documentation of similar fixes across the application
- [Streamlit Documentation on set_page_config](https://docs.streamlit.io/library/api-reference/utilities/st.set_page_config)

## Testing

After applying the fix, we verified:
- The Analytics Dashboard page loads without errors
- All functionality and styling are preserved
- No regression in other pages

## Preventative Measures

To prevent similar issues in the future:
1. Added clear comments about the `st.set_page_config()` requirement in all Streamlit pages
2. Updated documentation for developers with best practices for Streamlit page configuration
3. Considered implementing a linting rule or pre-commit hook to catch multiple `set_page_config()` calls
