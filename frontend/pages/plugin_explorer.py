# frontend/pages/plugin_explorer.py
import streamlit as st
import requests
from datetime import datetime
import json

# Constants
PLUGIN_METADATA_URL = "http://localhost:8000/plugins/execute"
CACHE_EXPIRY_MINUTES = 30

# Custom CSS
def inject_custom_css():
    st.markdown("""
    <style>
        .plugin-card {
            border-radius: 10px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            border-left: 4px solid #6e48aa;
        }
        .plugin-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 12px rgba(0,0,0,0.15);
        }
        .tag {
            display: inline-block;
            background: #f0f2f6;
            border-radius: 4px;
            padding: 2px 8px;
            margin-right: 6px;
            font-size: 0.8em;
            color: #555;
        }
        .stButton>button {
            transition: all 0.3s;
        }
        .stButton>button:hover {
            transform: scale(1.02);
        }
    </style>
    """, unsafe_allow_html=True)

# Cached data fetch
@st.cache_data(ttl=CACHE_EXPIRY_MINUTES * 60)
def fetch_plugin_metadata():
    try:
        response = requests.post(
            PLUGIN_METADATA_URL,
            json={"plugin": "plugin_metadata", "data": "_"},
            timeout=10
        )
        response.raise_for_status()
        return response.json().get("plugins", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load plugin metadata: {str(e)}")
        return None

def render_plugin_card(plugin):
    with st.container():
        st.markdown(f"""
        <div class="plugin-card">
            <h3>🔌 {plugin.get('name', 'Unnamed Plugin')}</h3>
            <p>{plugin.get('description', 'No description available')}</p>
            <div style="margin-bottom: 0.5rem;">
                <span class="tag">Author: {plugin.get('author', 'Anonymous')}</span>
                <span class="tag">Version: {plugin.get('version', '1.0')}</span>
                <span class="tag">Last Updated: {plugin.get('updated_at', 'N/A')}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        with st.expander("📝 Details & Examples"):
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown("**📦 Requirements**")
                if 'requirements' in plugin:
                    st.code("\n".join(plugin['requirements']), language="bash")
                else:
                    st.info("No special requirements")
                
                st.markdown("**⚙️ Parameters**")
                if 'parameters' in plugin:
                    st.json(plugin['parameters'])
                else:
                    st.info("No parameters defined")
            
            with col2:
                st.markdown("**💡 Example Usage**")
                st.code(plugin.get("example", "# No example provided"), 
                       language=plugin.get("language", "python"))
                
                if st.button(f"🚀 Run {plugin['name']}", key=f"run_{plugin['name']}"):
                    handle_plugin_execution(plugin)

def handle_plugin_execution(plugin):
    with st.spinner(f"Executing {plugin['name']}..."):
        try:
            # Add execution logic here
            st.session_state.setdefault('execution_history', []).append({
                'plugin': plugin['name'],
                'timestamp': datetime.now().isoformat()
            })
            
            # Simulate execution - replace with actual API call
            st.success(f"✅ {plugin['name']} executed successfully!")
            st.balloons()
            
        except Exception as e:
            st.error(f"Failed to execute plugin: {str(e)}")

def render_sidebar():
    with st.sidebar:
        st.title("🔍 Explorer Filters")
        
        # Search functionality
        search_query = st.text_input("Search plugins", placeholder="Filter by name/description")
        
        # Category filter
        categories = ["All", "Data", "ML", "API", "Utility"]
        selected_category = st.selectbox("Category", categories)
        
        # Sort options
        sort_by = st.radio("Sort by", ["Recently Added", "Most Popular", "A-Z"])
        
        st.markdown("---")
        st.markdown("**System Info**")
        st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        if st.checkbox("Show debug info"):
            st.json(st.session_state.get('execution_history', []))

def main():
    st.set_page_config(
        page_title="🔍 Plugin Explorer", 
        page_icon="🧩", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    inject_custom_css()
    st.title("🧩 Plugin Explorer")
    st.caption("Browse and execute available plugins")
    
    render_sidebar()
    
    plugins = fetch_plugin_metadata()
    if plugins is None:
        st.warning("Unable to load plugins. Please try again later.")
        return
    
    if not plugins:
        st.info("No plugins available. Check back later!")
        return
    
    # Apply filters (mock implementation - adapt to your data structure)
    filtered_plugins = plugins
    # if search_query:
    #     filtered_plugins = [p for p in plugins if search_query.lower() in p['name'].lower()]
    # if selected_category != "All":
    #     filtered_plugins = [p for p in filtered_plugins if p.get('category') == selected_category]
    
    # Display plugins in a grid
    cols = st.columns(2)
    for idx, plugin in enumerate(filtered_plugins):
        with cols[idx % 2]:
            render_plugin_card(plugin)

if __name__ == "__main__":
    main()