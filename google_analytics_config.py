# Google Analytics Configuration
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
