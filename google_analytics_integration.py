import streamlit as st
import streamlit.components.v1 as components

@st.cache_resource
def add_google_analytics(tracking_id, debug=False):
    """
    Add Google Analytics 4 to Streamlit app with optimized loading
    
    Args:
        tracking_id (str): Your Google Analytics tracking ID (e.g., 'G-XXXXXXXXXX')
        debug (bool): Enable debug mode for testing
    """
    
    # Optimized Google Analytics 4 tracking code with deferred loading
    ga_code = f"""
    <!-- Optimized Google tag (gtag.js) -->
    <script>
      // Initialize GA asynchronously to avoid blocking
      (function() {{
        var script = document.createElement('script');
        script.async = true;
        script.src = 'https://www.googletagmanager.com/gtag/js?id={tracking_id}';
        script.onload = function() {{
          window.dataLayer = window.dataLayer || [];
          function gtag(){{dataLayer.push(arguments);}}
          gtag('js', new Date());

          gtag('config', '{tracking_id}', {{
            'debug_mode': {str(debug).lower()},
            'send_page_view': true,
            'anonymize_ip': true,
            'allow_google_signals': false,
            'allow_ad_personalization_signals': false,
            'transport_type': 'beacon'  // Optimize for performance
          }});
          
          // Track custom events with error handling
          window.trackEvent = function(event_name, parameters = {{}}) {{
            try {{
              gtag('event', event_name, parameters);
              {f"console.log('GA Event:', event_name, parameters);" if debug else ""}
            }} catch(e) {{
              {f"console.error('GA Error:', e);" if debug else ""}
            }}
          }};
          
          {f"console.log('Google Analytics loaded with ID: {tracking_id}');" if debug else ""}
        }};
        document.head.appendChild(script);
      }})();
      
      // Fallback trackEvent for when GA is not loaded
      window.trackEvent = window.trackEvent || function() {{
        {f"console.log('GA not loaded, event skipped:', arguments);" if debug else ""}
      }};
    </script>
    """
    
    # Inject the Google Analytics code with minimal height
    try:
        components.html(ga_code, height=0)
        return True
    except Exception as e:
        if debug:
            st.warning(f"GA initialization failed: {e}")
        return False

def track_event(event_name, **parameters):
    """
    Track a custom event in Google Analytics
    
    Args:
        event_name (str): Name of the event
        **parameters: Additional parameters for the event
    """
    js_code = f"""
    <script>
      if (typeof window.trackEvent === 'function') {{
        window.trackEvent('{event_name}', {parameters});
      }}
    </script>
    """
    components.html(js_code, height=0)

def track_page_view(page_title, page_location=None):
    """
    Track a page view in Google Analytics
    
    Args:
        page_title (str): Title of the page
        page_location (str, optional): URL of the page
    """
    params = {'page_title': page_title}
    if page_location:
        params['page_location'] = page_location
    
    js_code = f"""
    <script>
      if (typeof gtag === 'function') {{
        gtag('event', 'page_view', {params});
      }}
    </script>
    """
    components.html(js_code, height=0)

def setup_enhanced_tracking():
    """
    Setup enhanced tracking for medical AI demo events
    """
    enhanced_code = """
    <script>
      // Enhanced tracking for medical AI demo
      document.addEventListener('DOMContentLoaded', function() {
        
        // Track model training interactions
        document.addEventListener('click', function(e) {
          if (e.target.closest('[data-testid*="expander"]')) {
            const expanderText = e.target.textContent || '';
            if (expanderText.includes('Model Training') || expanderText.includes('Addestramento')) {
              trackEvent('model_interaction', {
                'event_category': 'ML_Features',
                'event_label': 'Model Training Expanded'
              });
            }
            if (expanderText.includes('Clustering') || expanderText.includes('Analisi')) {
              trackEvent('clustering_interaction', {
                'event_category': 'ML_Features', 
                'event_label': 'Clustering Analysis Expanded'
              });
            }
            if (expanderText.includes('Code') || expanderText.includes('Codice')) {
              trackEvent('code_examples_interaction', {
                'event_category': 'Educational',
                'event_label': 'Code Examples Viewed'
              });
            }
          }
        });
        
        // Track button clicks
        document.addEventListener('click', function(e) {
          if (e.target.tagName === 'BUTTON') {
            const buttonText = e.target.textContent || '';
            if (buttonText.includes('Analytics') || buttonText.includes('Visitatori')) {
              trackEvent('analytics_clicked', {
                'event_category': 'Navigation',
                'event_label': 'Analytics Dashboard'
              });
            }
          }
        });
        
        // Track scroll depth
        let maxScroll = 0;
        window.addEventListener('scroll', function() {
          const scrollPercent = Math.round((window.scrollY / (document.body.scrollHeight - window.innerHeight)) * 100);
          if (scrollPercent > maxScroll && scrollPercent % 25 === 0) {
            maxScroll = scrollPercent;
            trackEvent('scroll_depth', {
              'event_category': 'Engagement',
              'event_label': scrollPercent + '% Scrolled'
            });
          }
        });
        
        // Track time on page
        let startTime = Date.now();
        window.addEventListener('beforeunload', function() {
          const timeSpent = Math.round((Date.now() - startTime) / 1000);
          trackEvent('time_on_page', {
            'event_category': 'Engagement',
            'event_label': 'Time Spent',
            'value': timeSpent
          });
        });
        
      });
    </script>
    """
    components.html(enhanced_code, height=0)

def create_ga_config_file():
    """Create a configuration file for Google Analytics setup"""
    config_content = '''# Google Analytics Configuration
# Per configurare Google Analytics per la tua app Streamlit:

# 1. Vai su https://analytics.google.com/
# 2. Crea una nuova proprietà per il tuo sito web
# 3. Ottieni il tuo Tracking ID (es. G-XXXXXXXXXX)  
# 4. Sostituisci 'YOUR_GA_TRACKING_ID' nel codice sotto

# Esempio di utilizzo nell'app principale:

from google_analytics_integration import add_google_analytics, track_event

# Aggiungi all'inizio della tua app Streamlit
add_google_analytics('YOUR_GA_TRACKING_ID', debug=True)

# Traccia eventi personalizzati
track_event('model_training_started', 
           event_category='ML_Features',
           event_label='Random Forest Model',
           value=1)

track_event('feature_used',
           event_category='User_Interaction', 
           event_label='Clustering Analysis',
           custom_parameter='k_means_3_clusters')

# PRIVACY E GDPR COMPLIANCE:
# - anonymize_ip è abilitato automaticamente
# - allow_google_signals è disabilitato 
# - allow_ad_personalization_signals è disabilitato
# Questo assicura la conformità GDPR per gli utenti europei
'''
    
    with open('google_analytics_config.py', 'w', encoding='utf-8') as f:
        f.write(config_content)
    
    return "google_analytics_config.py"
