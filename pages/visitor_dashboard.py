import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from analytics_tracker import AnalyticsTracker
from enhanced_analytics import EnhancedAnalyticsTracker

# Import notification manager if available
try:
    from notification_manager import NotificationManager
except ImportError:
    # Create a minimal notification manager if not available
    class NotificationManager:
        def __init__(self):
            pass
        
        def add_notification(self, message, notification_type="info"):
            pass

def load_visitor_data():
    """Load visitor data from analytics"""
    try:
        with open("analytics/usage_data.json", "r") as f:
            data = json.load(f)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        return {"sessions": [], "features": {}}

def create_visitor_dashboard():
    """Create the visitor analytics dashboard"""
    st.set_page_config(
        page_title="Visitor Analytics - Nino Medical AI",
        page_icon="📊",
        layout="wide"
    )
    
    # Navigation header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("📊 Visitor Analytics Dashboard")
        st.markdown("**Nino Medical AI Demo - Analytics Overview**")
    
    with col2:
        if st.button("🏥 Medical AI Demo", use_container_width=True):
            st.switch_page("app.py")
    
    with col3:
        if st.button("📝 Feedback Dashboard", use_container_width=True):
            st.switch_page("pages/feedback_dashboard.py")
    
    st.markdown("---")
    
    # Load data
    data = load_visitor_data()
    
    if not data["sessions"]:
        st.warning("Nessun dato sui visitatori disponibile ancora.")
        return
    
    # Convert to DataFrame
    sessions_df = pd.DataFrame(data["sessions"])
    sessions_df['timestamp'] = pd.to_datetime(sessions_df['timestamp'])
    sessions_df['date'] = sessions_df['timestamp'].dt.date
    sessions_df['hour'] = sessions_df['timestamp'].dt.hour
    
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_sessions = len(sessions_df)
        st.metric("🎯 Sessioni Totali", total_sessions)
    
    with col2:
        unique_users = sessions_df['user_id'].nunique()
        st.metric("👥 Utenti Unici", unique_users)
    
    with col3:
        # Sessions in last 7 days
        recent_sessions = len(sessions_df[sessions_df['timestamp'] > datetime.now() - timedelta(days=7)])
        st.metric("📅 Ultimi 7 Giorni", recent_sessions)
    
    with col4:
        # Sessions today
        today_sessions = len(sessions_df[sessions_df['date'] == datetime.now().date()])
        st.metric("📍 Oggi", today_sessions)
    
    st.markdown("---")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 Visite per Giorno")
        if len(sessions_df) > 0:
            daily_visits = sessions_df.groupby('date').size().reset_index(name='visits')
            daily_visits['date'] = pd.to_datetime(daily_visits['date'])
            
            fig = px.line(daily_visits, x='date', y='visits', 
                         title="Andamento Visite Giornaliere",
                         markers=True)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🕐 Visite per Ora")
        if len(sessions_df) > 0:
            hourly_visits = sessions_df.groupby('hour').size().reset_index(name='visits')
            
            fig = px.bar(hourly_visits, x='hour', y='visits',
                        title="Distribuzione Oraria delle Visite")
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
    
    # Feature Usage
    st.subheader("🔧 Utilizzo Funzionalità")
    if data["features"]:
        features_df = pd.DataFrame(list(data["features"].items()), 
                                 columns=['Feature', 'Usage'])
        
        # Translate feature names to Italian
        feature_translation = {
            "model_training_process": "Addestramento Modello",
            "clustering_analysis": "Analisi Clustering", 
            "ml_code_examples": "Esempi Codice ML"
        }
        
        features_df['Feature_IT'] = features_df['Feature'].map(feature_translation).fillna(features_df['Feature'])
        
        fig = px.bar(features_df, x='Feature_IT', y='Usage',
                    title="Funzionalità Più Utilizzate")
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    # Detailed Sessions Table
    st.subheader("📋 Dettagli Sessioni Recenti")
    if len(sessions_df) > 0:
        # Show last 10 sessions
        recent_sessions = sessions_df.tail(10).copy()
        recent_sessions['timestamp'] = recent_sessions['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        recent_sessions = recent_sessions[['timestamp', 'session_id', 'user_agent']]
        recent_sessions.columns = ['Data/Ora', 'ID Sessione', 'Browser']
        
        st.dataframe(recent_sessions, use_container_width=True)
    
    # Geographic Analysis
    st.subheader("🌍 Analisi Geografica")
    if 'geo_data' in sessions_df.columns:
        # Extract geographic data
        geo_info = []
        for _, row in sessions_df.iterrows():
            if pd.notna(row.get('geo_data')):
                geo_data = row['geo_data'] if isinstance(row['geo_data'], dict) else {}
                geo_info.append({
                    'Country': geo_data.get('country', 'Sconosciuto'),
                    'City': geo_data.get('city', 'Sconosciuto'),
                    'Region': geo_data.get('region', 'Sconosciuto')
                })
        
        if geo_info:
            geo_df = pd.DataFrame(geo_info)
            
            col1, col2 = st.columns(2)
            
            with col1:
                country_counts = geo_df['Country'].value_counts()
                fig = px.bar(x=country_counts.index, y=country_counts.values,
                           title="Visitatori per Paese")
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                city_counts = geo_df['City'].value_counts().head(10)
                fig = px.bar(x=city_counts.index, y=city_counts.values,
                           title="Top 10 Città")
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
    
    # Notifications
    st.subheader("🔔 Notifiche Visitatori")
    if 'notifications' in data and data['notifications']:
        notifications_df = pd.DataFrame(data['notifications'])
        notifications_df['timestamp'] = pd.to_datetime(notifications_df['timestamp'])
        
        # Show recent notifications
        recent_notifications = notifications_df.tail(5)
        
        for _, notification in recent_notifications.iterrows():
            timestamp = notification['timestamp'].strftime('%Y-%m-%d %H:%M:%S')
            message = notification['message']
            
            with st.container():
                st.info(f"**{timestamp}**: {message}")
    else:
        st.info("Nessuna notifica disponibile")
    
    # Browser Analysis
    st.subheader("🌐 Analisi Browser")
    if len(sessions_df) > 0:
        # Extract browser info from user_agent
        def extract_browser(user_agent):
            if 'unknown' in user_agent.lower():
                return 'Sconosciuto'
            elif 'edge' in user_agent.lower():
                return 'Microsoft Edge'
            elif 'chrome' in user_agent.lower():
                return 'Google Chrome'
            elif 'firefox' in user_agent.lower():
                return 'Mozilla Firefox'
            elif 'safari' in user_agent.lower():
                return 'Safari'
            else:
                return 'Altro'
        
        sessions_df['browser'] = sessions_df['user_agent'].apply(extract_browser)
        browser_counts = sessions_df['browser'].value_counts()
        
        fig = px.pie(values=browser_counts.values, names=browser_counts.index,
                    title="Distribuzione Browser")
        st.plotly_chart(fig, use_container_width=True)
    
    # Real-time Analytics
    st.subheader("⚡ Real-time Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Current active users estimation
        now = datetime.now()
        last_hour = now - timedelta(hours=1)
        active_users = len(sessions_df[sessions_df['timestamp'] > last_hour]) if len(sessions_df) > 0 else 0
        st.metric("🟢 Active Users (Last Hour)", active_users)
    
    with col2:
        # Average session duration estimation
        if len(sessions_df) > 0:
            avg_duration = "~5 min"  # Estimated based on typical Streamlit usage
        else:
            avg_duration = "N/A"
        st.metric("⏱️ Avg Session Duration", avg_duration)
    
    # Performance Insights
    st.subheader("📈 Performance Insights")
    
    insights = []
    
    if len(sessions_df) > 0:
        # Peak usage hour
        peak_hour = sessions_df['hour'].mode().iloc[0] if not sessions_df['hour'].mode().empty else 0
        insights.append(f"🕐 Peak usage hour: {peak_hour}:00")
        
        # Most active day
        if len(sessions_df) > 1:
            most_active_day = sessions_df.groupby('date').size().idxmax()
            insights.append(f"📅 Most active day: {most_active_day}")
        
        # Feature usage insights
        if data["features"]:
            most_used_feature = max(data["features"], key=data["features"].get)
            feature_translation = {
                "model_training_process": "Addestramento Modello",
                "clustering_analysis": "Analisi Clustering", 
                "ml_code_examples": "Esempi Codice ML"
            }
            translated_feature = feature_translation.get(most_used_feature, most_used_feature)
            insights.append(f"🔧 Most used feature: {translated_feature} ({data['features'][most_used_feature]} times)")
    
    if insights:
        for insight in insights:
            st.info(insight)
    else:
        st.info("📊 Collecting data for insights...")
    
    # Export functionality
    st.markdown("---")
    st.subheader("📤 Esporta Dati")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Scarica CSV Sessioni"):
            csv_data = sessions_df.to_csv(index=False)
            st.download_button(
                label="💾 Download CSV",
                data=csv_data,
                file_name=f"visitor_analytics_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
    
    with col2:
        if st.button("📋 Genera Report"):
            report = f"""
# Report Analytics Visitatori - Nino Medical AI
Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Statistiche Generali
- Sessioni Totali: {total_sessions}
- Utenti Unici: {unique_users}
- Sessioni Ultimi 7 Giorni: {recent_sessions}
- Sessioni Oggi: {today_sessions}
- Utenti Attivi (Ultima Ora): {active_users}

## Top 3 Funzionalità
{chr(10).join([f"- {k}: {v} utilizzi" for k, v in sorted(data['features'].items(), key=lambda x: x[1], reverse=True)[:3]]) if data['features'] else "Nessuna funzionalità tracciata"}

## Insights
{chr(10).join([f"- {insight}" for insight in insights]) if insights else "Nessun insight disponibile"}

## Note
Questo report è generato automaticamente dal sistema di analytics del Nino Medical AI Demo.
Tutti i dati sono anonimi e rispettano la privacy degli utenti.
            """
            st.download_button(
                label="💾 Download Report",
                data=report,
                file_name=f"analytics_report_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )
    
    with col3:
        if st.button("📧 Email Report"):
            st.info("📧 Email functionality would be implemented here in production")
            st.code("# Email integration example\n# Would send report to admin email", language="python")

if __name__ == "__main__":
    create_visitor_dashboard()
