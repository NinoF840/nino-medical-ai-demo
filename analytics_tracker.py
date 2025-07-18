import streamlit as st
import datetime
import json
import os
import uuid

class AnalyticsTracker:
    def __init__(self):
        self.analytics_file = "analytics/usage_data.json"
        self.ensure_analytics_dir()
        self.init_session()
    
    def ensure_analytics_dir(self):
        """Ensure analytics directory exists"""
        os.makedirs("analytics", exist_ok=True)
        if not os.path.exists(self.analytics_file):
            with open(self.analytics_file, 'w') as f:
                json.dump({"sessions": [], "features": {}}, f)
    
    def init_session(self):
        """Initialize session tracking"""
        if 'session_id' not in st.session_state:
            st.session_state.session_id = str(uuid.uuid4())
        if 'session_start' not in st.session_state:
            st.session_state.session_start = datetime.datetime.now()
            self.track_session()
    
    def track_session(self, user_id=None):
        """Track user session"""
        session_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": user_id or st.session_state.get('user_id', 'anonymous'),
            "session_id": st.session_state.session_id,
            "user_agent": st.context.headers.get("user-agent", "unknown") if hasattr(st.context, 'headers') else "unknown"
        }
        
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"sessions": [], "features": {}}
        
        data["sessions"].append(session_data)
        
        with open(self.analytics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def track_feature_usage(self, feature_name):
        """Track feature usage"""
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"sessions": [], "features": {}}
        
        if feature_name not in data["features"]:
            data["features"][feature_name] = 0
        
        data["features"][feature_name] += 1
        
        with open(self.analytics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_analytics_summary(self):
        """Get analytics summary"""
        try:
            with open(self.analytics_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "total_sessions": 0,
                "unique_users": 0,
                "feature_usage": {},
                "last_30_days": 0
            }
        
        return {
            "total_sessions": len(data["sessions"]),
            "unique_users": len(set(s.get("user_id", "anonymous") for s in data["sessions"])),
            "feature_usage": data["features"],
            "last_30_days": self._get_recent_sessions(30)
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

# Initialize global tracker
if 'analytics_tracker' not in st.session_state:
    st.session_state.analytics_tracker = AnalyticsTracker()
