import streamlit as st
import json
import os
from datetime import datetime, timedelta

def show_visitor_counter():
    """Display a simple visitor counter in the main app"""
    try:
        with open("analytics/usage_data.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {"sessions": [], "features": {}}
    
    total_visitors = len(data["sessions"])
    
    # Calculate recent visitors (last 7 days)
    if data["sessions"]:
        recent_count = 0
        cutoff = datetime.now() - timedelta(days=7)
        
        for session in data["sessions"]:
            try:
                session_time = datetime.fromisoformat(session["timestamp"])
                if session_time > cutoff:
                    recent_count += 1
            except (ValueError, KeyError):
                continue
    else:
        recent_count = 0
    
    # Display in a nice format
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; text-align: center;">
            <h3 style="color: #1f77b4; margin: 0;">👥 Visitatori Totali</h3>
            <h2 style="color: #1f77b4; margin: 10px 0;">{total_visitors}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div style="background-color: #e8f5e8; padding: 20px; border-radius: 10px; text-align: center;">
            <h3 style="color: #2ca02c; margin: 0;">📅 Ultimi 7 Giorni</h3>
            <h2 style="color: #2ca02c; margin: 10px 0;">{recent_count}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        if st.button("📊 Visualizza Analytics Complete", key="analytics_button"):
            st.markdown("""
            ### 🔗 Dashboard Analytics
            Per vedere le statistiche complete dei visitatori, esegui:
            
            ```bash
            streamlit run visitor_dashboard.py --server.port 8502
            ```
            
            Questo aprirà la dashboard completa su una porta separata!
            """)

def get_visitor_summary():
    """Get a simple visitor summary for display"""
    try:
        with open("analytics/usage_data.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "total_visitors": 0,
            "recent_visitors": 0,
            "top_feature": "Nessuna"
        }
    
    total_visitors = len(data["sessions"])
    
    # Recent visitors (last 7 days)
    recent_count = 0
    cutoff = datetime.now() - timedelta(days=7)
    
    for session in data["sessions"]:
        try:
            session_time = datetime.fromisoformat(session["timestamp"])
            if session_time > cutoff:
                recent_count += 1
        except (ValueError, KeyError):
            continue
    
    # Top feature
    top_feature = "Nessuna"
    if data["features"]:
        top_feature_key = max(data["features"], key=data["features"].get)
        feature_names = {
            "model_training_process": "Addestramento Modello",
            "clustering_analysis": "Analisi Clustering", 
            "ml_code_examples": "Esempi Codice ML"
        }
        top_feature = feature_names.get(top_feature_key, top_feature_key)
    
    return {
        "total_visitors": total_visitors,
        "recent_visitors": recent_count,
        "top_feature": top_feature
    }
