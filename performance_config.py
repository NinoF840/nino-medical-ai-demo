# Performance Optimization Configuration for Nino Medical AI Demo
"""
This file contains configuration settings to optimize the performance
of the Streamlit application, reducing load times and improving responsiveness.
"""

# Cache Settings
CACHE_SETTINGS = {
    'max_entries': 100,  # Maximum cached entries per function
    'ttl': 3600,  # Time to live in seconds (1 hour)
    'show_spinner': False,  # Hide loading spinners for better UX
}

# Analytics Settings
ANALYTICS_SETTINGS = {
    'enable_tracking': True,
    'batch_size': 10,  # Batch analytics events
    'max_sessions': 500,  # Keep only last 500 sessions
    'async_processing': True,
}

# Google Analytics Settings
GA_SETTINGS = {
    'defer_loading': True,
    'use_beacon': True,  # Use beacon API for better performance
    'debug_mode': False,  # Set to True only for development
    'track_scroll': False,  # Disable scroll tracking to reduce events
}

# Data Generation Settings
DATA_SETTINGS = {
    'default_patients': 100,
    'cache_enabled': True,
    'use_compact_json': True,
}

# UI Settings
UI_SETTINGS = {
    'lazy_load_components': True,
    'minimize_recompute': True,
    'use_container_width': True,
}

# Performance Monitoring
MONITORING = {
    'track_load_times': True,
    'log_performance_warnings': False,  # Disable to reduce console noise
    'memory_threshold': 100,  # MB
}

# Streamlit Configuration Recommendations
STREAMLIT_CONFIG = {
    'server.enableCORS': False,
    'server.enableXsrfProtection': False,
    'browser.gatherUsageStats': False,
    'client.caching': True,
    'client.displayEnabled': True,
    'runner.magicEnabled': True,
    'runner.installTracer': False,
}

def get_optimized_page_config():
    """Return optimized page configuration for Streamlit"""
    return {
        'page_title': 'Nino Medical AI Demo',
        'page_icon': '🏥',
        'layout': 'wide',
        'initial_sidebar_state': 'expanded',
        'menu_items': {
            'Get Help': 'https://github.com/NinoF840/nino-medical-ai-demo',
            'Report a bug': 'https://github.com/NinoF840/nino-medical-ai-demo/issues',
            'About': '''
            # Nino Medical AI Demo
            An optimized open-source platform for medical AI education.
            
            **Performance Optimized**: Lazy loading, caching, and async processing
            '''
        }
    }

def apply_performance_optimizations():
    """Apply performance optimizations to the Streamlit app"""
    import streamlit as st
    
    # Set page config with optimizations
    if 'page_config_set' not in st.session_state:
        st.set_page_config(**get_optimized_page_config())
        st.session_state.page_config_set = True
    
    # Hide Streamlit style elements for cleaner UI and better performance
    hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    .stDecoration {visibility: hidden;}
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
    
    return True

# Performance Tips for Developers
PERFORMANCE_TIPS = """
## Performance Optimization Tips

1. **Caching**: Use @st.cache_data for data processing and @st.cache_resource for ML models
2. **Lazy Loading**: Import heavy modules only when needed
3. **Batch Operations**: Process multiple operations together
4. **Minimize Recomputation**: Use session state to store expensive calculations
5. **Async Operations**: Use threading for non-blocking operations
6. **Data Chunking**: Process large datasets in smaller chunks
7. **Component Optimization**: Use container_width=True for responsive design
8. **Memory Management**: Clear caches periodically and limit data retention

## Implemented Optimizations

✅ Lazy loading of analytics modules
✅ Cached data generation with @st.cache_data
✅ Optimized Google Analytics with deferred loading
✅ Thread-safe analytics tracking
✅ Compact JSON storage
✅ Memory-efficient data structures
✅ Error handling to prevent crashes
✅ Performance monitoring capabilities
"""

if __name__ == "__main__":
    print("Performance Configuration for Nino Medical AI Demo")
    print("=" * 50)
    print(PERFORMANCE_TIPS)
