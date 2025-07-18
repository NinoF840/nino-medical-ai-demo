#!/usr/bin/env python3
"""
Script per mostrare le statistiche dei visitatori
"""
import json
import pandas as pd
from datetime import datetime, timedelta

def show_visitor_stats():
    """Mostra le statistiche dei visitatori"""
    try:
        with open("analytics/usage_data.json", "r") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ Nessun dato sui visitatori trovato!")
        return
    
    sessions = data["sessions"]
    features = data["features"]
    
    print("🏥 NINO MEDICAL AI DEMO - STATISTICHE VISITATORI")
    print("=" * 50)
    
    # Statistiche generali
    total_sessions = len(sessions)
    print(f"📊 Sessioni totali: {total_sessions}")
    
    if total_sessions == 0:
        print("❌ Nessuna sessione registrata ancora.")
        return
    
    # Calcola visitatori recenti
    recent_count = 0
    cutoff = datetime.now() - timedelta(days=7)
    
    for session in sessions:
        try:
            session_time = datetime.fromisoformat(session["timestamp"])
            if session_time > cutoff:
                recent_count += 1
        except (ValueError, KeyError):
            continue
    
    print(f"📅 Visitatori ultimi 7 giorni: {recent_count}")
    
    # Analisi browser
    browsers = {}
    for session in sessions:
        user_agent = session.get("user_agent", "unknown")
        if 'edge' in user_agent.lower():
            browser = 'Microsoft Edge'
        elif 'chrome' in user_agent.lower():
            browser = 'Google Chrome'
        elif 'firefox' in user_agent.lower():
            browser = 'Mozilla Firefox'
        elif 'safari' in user_agent.lower():
            browser = 'Safari'
        elif 'unknown' in user_agent.lower():
            browser = 'Sconosciuto'
        else:
            browser = 'Altro'
        
        browsers[browser] = browsers.get(browser, 0) + 1
    
    print(f"\n🌐 Browser utilizzati:")
    for browser, count in browsers.items():
        print(f"   • {browser}: {count} sessioni")
    
    # Funzionalità più utilizzate
    print(f"\n🔧 Funzionalità più utilizzate:")
    if features:
        feature_names = {
            "model_training_process": "Addestramento Modello",
            "clustering_analysis": "Analisi Clustering", 
            "ml_code_examples": "Esempi Codice ML"
        }
        
        for feature, count in sorted(features.items(), key=lambda x: x[1], reverse=True):
            italian_name = feature_names.get(feature, feature)
            print(f"   • {italian_name}: {count} utilizzi")
    else:
        print("   • Nessuna funzionalità utilizzata ancora")
    
    # Ultime sessioni
    print(f"\n📋 Ultime 5 sessioni:")
    recent_sessions = sorted(sessions, key=lambda x: x["timestamp"], reverse=True)[:5]
    
    for i, session in enumerate(recent_sessions, 1):
        timestamp = datetime.fromisoformat(session["timestamp"])
        formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        session_id = session["session_id"][:8]  # Mostra solo primi 8 caratteri
        print(f"   {i}. {formatted_time} - ID: {session_id}...")
    
    print(f"\n" + "=" * 50)
    print("💡 Per vedere la dashboard completa, esegui:")
    print("   streamlit run visitor_dashboard.py --server.port 8502")
    print("📊 Per vedere l'app principale, esegui:")
    print("   streamlit run app.py")

if __name__ == "__main__":
    show_visitor_stats()
