import streamlit as st
import datetime
import json
import os
import uuid
from functools import lru_cache
import threading
from contextlib import contextmanager

class AnalyticsTracker:
    def __init__(self):
        self.analytics_file = "analytics/usage_data.json"
        self._lock = threading.Lock()
        self._ensure_analytics_dir()
        self._init_session()
    
    @contextmanager
    def _file_lock(self):
        """Thread-safe file access"""
        with self._lock:
            yield
    
    def _ensure_analytics_dir(self):
        """Optimized analytics directory setup"""
        try:
            os.makedirs("analytics", exist_ok=True)
            if not os.path.exists(self.analytics_file):
                with self._file_lock():
                    with open(self.analytics_file, 'w') as f:
                        json.dump({"sessions": [], "features": {}}, f)
        except Exception:
            # Fail silently - analytics should not break the app
            pass
    
    def _init_session(self):
        """Optimized session initialization"""
        try:
            if 'session_id' not in st.session_state:
                st.session_state.session_id = str(uuid.uuid4())
            if 'session_start' not in st.session_state:
                st.session_state.session_start = datetime.datetime.now()
                # Track session asynchronously to avoid blocking
                self._track_session_async()
        except Exception:
            # Fail silently - session tracking should not break the app
            pass
    
    def _track_session_async(self, user_id=None):
        """Async session tracking to avoid blocking main thread"""
        try:
            session_data = {
                "timestamp": datetime.datetime.now().isoformat(),
                "user_id": user_id or st.session_state.get('user_id', 'anonymous'),
                "session_id": st.session_state.session_id,
                "user_agent": "streamlit-app"
            }
            
            # Use cached data loading
            data = self._load_analytics_data()
            data["sessions"].append(session_data)
            
            # Limit session history to prevent file bloat
            if len(data["sessions"]) > 1000:
                data["sessions"] = data["sessions"][-500:]  # Keep last 500
            
            self._save_analytics_data(data)
        except Exception:
            # Fail silently
            pass
    
    @lru_cache(maxsize=1)
    def _load_analytics_data(self):
        """Cached analytics data loading"""
        try:
            if os.path.exists(self.analytics_file):
                with open(self.analytics_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {"sessions": [], "features": {}}
    
    def _save_analytics_data(self, data):
        """Optimized data saving"""
        try:
            with self._file_lock():
                with open(self.analytics_file, 'w') as f:
                    json.dump(data, f, separators=(',', ':'))  # Compact format
                # Clear cache to reload fresh data
                self._load_analytics_data.cache_clear()
        except Exception:
            # Fail silently
            pass
    
    def track_session(self, user_id=None):
        """Public session tracking interface"""
        try:
            self._track_session_async(user_id)
        except Exception:
            pass
    
    def track_feature_usage(self, feature_name):
        """Optimized feature usage tracking"""
        try:
            data = self._load_analytics_data()
            
            if feature_name not in data["features"]:
                data["features"][feature_name] = 0
            
            data["features"][feature_name] += 1
            self._save_analytics_data(data)
        except Exception:
            # Fail silently
            pass
    
    @lru_cache(maxsize=1, typed=True)
    def get_analytics_summary(self):
        """Cached analytics summary"""
        try:
            data = self._load_analytics_data()
            
            return {
                "total_sessions": len(data.get("sessions", [])),
                "unique_users": len(set(s.get("user_id", "anonymous") for s in data.get("sessions", []))),
                "feature_usage": data.get("features", {}),
                "last_30_days": self._get_recent_sessions(30)
            }
        except Exception:
            return {
                "total_sessions": 0,
                "unique_users": 0,
                "feature_usage": {},
                "last_30_days": 0
            }
    
    def _get_recent_sessions(self, days):
        """Optimized recent sessions calculation"""
        try:
            cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
            data = self._load_analytics_data()
            
            count = 0
            for session in data.get("sessions", []):
                try:
                    session_time = datetime.datetime.fromisoformat(session["timestamp"])
                    if session_time > cutoff:
                        count += 1
                except (KeyError, ValueError):
                    continue
            
            return count
        except Exception:
            return 0

# Initialize global tracker
if 'analytics_tracker' not in st.session_state:
    st.session_state.analytics_tracker = AnalyticsTracker()
