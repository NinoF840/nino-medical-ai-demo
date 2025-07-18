import streamlit as st
import json
import datetime
import os

class FeedbackCollector:
    def __init__(self):
        self.feedback_file = "analytics/feedback.json"
        self.ensure_feedback_dir()

    def ensure_feedback_dir(self):
        """Ensure feedback directory exists"""
        os.makedirs("analytics", exist_ok=True)
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'w') as f:
                json.dump({"feedback": []}, f)

    def collect_user_feedback(self):
        """Collect user feedback through Streamlit interface"""
        st.sidebar.markdown("---")
        st.sidebar.header("📝 Feedback")

        with st.sidebar.expander("Help us improve!"):
            # Rating system
            rating = st.select_slider(
                "How would you rate this tool?",
                options=["Poor", "Fair", "Good", "Very Good", "Excellent"],
                value="Good"
            )

            # Usage type
            usage_type = st.selectbox(
                "I am using this tool for:",
                ["Learning/Education", "Research", "Teaching", "Industry Application", "Other"]
            )

            # Feedback text
            feedback_text = st.text_area(
                "Any suggestions or comments?",
                placeholder="Tell us what you think..."
            )

            # Submit feedback
            if st.button("Submit Feedback"):
                feedback_data = {
                    "timestamp": datetime.datetime.now().isoformat(),
                    "rating": rating,
                    "usage_type": usage_type,
                    "feedback": feedback_text,
                    "session_id": st.session_state.get('session_id', 'unknown')
                }
                self.save_feedback(feedback_data)
                st.success("Thank you for your feedback!")

    def save_feedback(self, feedback_data):
        """Save feedback to JSON file"""
        try:
            with open(self.feedback_file, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {"feedback": []}

        data["feedback"].append(feedback_data)

        with open(self.feedback_file, 'w') as f:
            json.dump(data, f, indent=2)

# Initialize global feedback collector
if 'feedback_collector' not in st.session_state:
    st.session_state.feedback_collector = FeedbackCollector()

