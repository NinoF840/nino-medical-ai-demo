import streamlit as st
import datetime
import json
import os
import uuid
import requests
import time

class EnhancedAnalyticsTracker:
    def __init__(self):
        self.analytics_file = "analytics/usage_data.json"
        self.geo_file = "analytics/geo_data.json"
        self.ensure_analytics_dir()
        self.init_session()
    
    def ensure_analytics_dir(self):
        """Ensure analytics directory exists"""
        os.makedirs("analytics", exist_ok=True)
        if not os.path.exists(self.analytics_file):
            with open(self.analytics_file, 'w') as f:
                json.dump({"sessions": [], "features": {}, "notifications": []}, f)
        if not os.path.exists(self.geo_file):
            with open(self.geo_file, 'w') as f:
                json.dump({"geo_sessions": []}, f)
    
    def get_visitor_ip(self):
        """Get visitor IP address safely"""
        try:
            # Try to get real IP from Streamlit headers
            if hasattr(st, 'context') and hasattr(st.context, 'headers'):
                # Check for forwarded IP first
                forwarded_for = st.context.headers.get('x-forwarded-for')
                if forwarded_for:
                    return forwarded_for.split(',')[0].strip()
                
                # Check for real IP
                real_ip = st.context.headers.get('x-real-ip')
                if real_ip:
                    return real_ip
            
            # Fallback: get public IP
            response = requests.get('https://httpbin.org/ip', timeout=5)
            if response.status_code == 200:
                return response.json().get('origin', 'unknown')
        except Exception:
            pass
        return 'unknown'
    
    def get_geolocation(self, ip_address):
        """Get geolocation data from IP"""
        if ip_address == 'unknown' or ip_address == '127.0.0.1':
            return {
                "country": "Locale",
                "region": "Sviluppo",
                "city": "Localhost",
                "timezone": "UTC"
            }
        
        try:
            # Using a free IP geolocation service
            response = requests.get(
                f'http://ip-api.com/json/{ip_address}?fields=country,regionName,city,timezone,status',
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    return {
                        "country": data.get('country', 'Sconosciuto'),
                        "region": data.get('regionName', 'Sconosciuto'),
                        "city": data.get('city', 'Sconosciuto'),
                        "timezone": data.get('timezone', 'UTC')
                    }
        except Exception as e:
            print(f"Errore geolocalizzazione: {e}")
        
        return {
            "country": "Sconosciuto",
            "region": "Sconosciuto", 
            "city": "Sconosciuto",
            "timezone": "UTC"
        }
    
    def init_session(self):
        """Initialize session tracking with geolocation"""
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        if 'session_start' not in st.session_state:
            st.session_state.session_start = datetime.datetime.now()
            
            # Track session with geolocation
            visitor_ip = self.get_visitor_ip()
            geo_data = self.get_geolocation(visitor_ip)
            self.track_session_with_geo(visitor_ip, geo_data)
            
            # Send notification for new visitor
            self.send_visitor_notification(geo_data)
    
    def track_session_with_geo(self, ip_address, geo_data, user_id=None):
        """Track user session with geolocation"""
        session_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": user_id or st.session_state.get('user_id', 'anonymous'),
            "session_id": st.session_state.session_id,
            "user_agent": st.context.headers.get("user-agent", "unknown") if hasattr(st.context, 'headers') else "unknown",
            "ip_address": ip_address,
            "geo_data": geo_data
        }
        
        # Update main analytics file
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"sessions": [], "features": {}, "notifications": []}
        
        data["sessions"].append(session_data)
        
        with open(self.analytics_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Update geo file
        try:
            with open(self.geo_file, 'r') as f:
                geo_file_data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            geo_file_data = {"geo_sessions": []}
        
        geo_file_data["geo_sessions"].append(session_data)
        
        with open(self.geo_file, 'w') as f:
            json.dump(geo_file_data, f, indent=2)
    
    def send_visitor_notification(self, geo_data):
        """Send notification about new visitor"""
        notification = {
            "timestamp": datetime.datetime.now().isoformat(),
            "type": "new_visitor",
            "message": f"🌍 Nuovo visitatore da {geo_data['city']}, {geo_data['country']}",
            "geo_data": geo_data
        }
        
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"sessions": [], "features": {}, "notifications": []}
        
        if "notifications" not in data:
            data["notifications"] = []
        
        data["notifications"].append(notification)
        
        # Keep only last 100 notifications
        data["notifications"] = data["notifications"][-100:]
        
        with open(self.analytics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def track_feature_usage(self, feature_name):
        """Track feature usage"""
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"sessions": [], "features": {}, "notifications": []}
        
        if feature_name not in data["features"]:
            data["features"][feature_name] = 0
        
        data["features"][feature_name] += 1
        
        with open(self.analytics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_geo_analytics(self):
        """Get geographic analytics"""
        try:
            with open(self.geo_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"countries": {}, "cities": {}, "regions": {}}
        
        countries = {}
        cities = {}
        regions = {}
        
        for session in data.get("geo_sessions", []):
            geo = session.get("geo_data", {})
            
            country = geo.get("country", "Sconosciuto")
            city = geo.get("city", "Sconosciuto")
            region = geo.get("region", "Sconosciuto")
            
            countries[country] = countries.get(country, 0) + 1
            cities[city] = cities.get(city, 0) + 1
            regions[region] = regions.get(region, 0) + 1
        
        return {
            "countries": countries,
            "cities": cities,
            "regions": regions
        }
    
    def get_recent_notifications(self, limit=10):
        """Get recent notifications"""
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []
        
        notifications = data.get("notifications", [])
        return sorted(notifications, key=lambda x: x["timestamp"], reverse=True)[:limit]
    
    def get_analytics_summary(self):
        """Get enhanced analytics summary"""
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "total_sessions": 0,
                "unique_users": 0,
                "feature_usage": {},
                "last_30_days": 0,
                "countries": {},
                "notifications_count": 0
            }
        
        geo_data = self.get_geo_analytics()
        
        return {
            "total_sessions": len(data["sessions"]),
            "unique_users": len(set(s.get("user_id", "anonymous") for s in data["sessions"])),
            "feature_usage": data["features"],
            "last_30_days": self._get_recent_sessions(30),
            "countries": geo_data["countries"],
            "notifications_count": len(data.get("notifications", []))
        }
    
    def _get_recent_sessions(self, days):
        """Get sessions from last N days"""
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return 0
        
        recent_sessions = [
            s for s in data["sessions"]
            if datetime.datetime.fromisoformat(s["timestamp"]) > cutoff
        ]
        
        return len(recent_sessions)
