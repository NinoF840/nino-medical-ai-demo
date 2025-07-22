import streamlit as st
import json
import datetime
import os
import re
import uuid
from typing import Dict, List, Optional
import pandas as pd

class EnhancedFeedbackCollector:
    def __init__(self):
        self.feedback_file = "analytics/feedback.json"
        self.contact_file = "analytics/user_contacts.json"
        self.ensure_feedback_dir()

    def ensure_feedback_dir(self):
        """Ensure feedback directory exists"""
        os.makedirs("analytics", exist_ok=True)
        
        # Initialize feedback file
        if not os.path.exists(self.feedback_file):
            with open(self.feedback_file, 'w') as f:
                json.dump({
                    "feedback": [],
                    "stats": {
                        "total_feedback": 0,
                        "average_rating": 0,
                        "last_updated": datetime.datetime.now().isoformat()
                    }
                }, f)
        
        # Initialize contacts file
        if not os.path.exists(self.contact_file):
            with open(self.contact_file, 'w') as f:
                json.dump({
                    "contacts": [],
                    "newsletter_subscribers": [],
                    "stats": {
                        "total_contacts": 0,
                        "newsletter_subscribers": 0,
                        "last_updated": datetime.datetime.now().isoformat()
                    }
                }, f)

    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def collect_user_feedback(self):
        """Enhanced user feedback collection through Streamlit interface"""
        st.sidebar.markdown("---")
        st.sidebar.header("📝 User Feedback & Contact")

        with st.sidebar.expander("💬 Share Your Feedback", expanded=False):
            self._render_feedback_form()

        with st.sidebar.expander("📧 Stay Connected", expanded=False):
            self._render_contact_form()

        with st.sidebar.expander("📊 Feedback Stats", expanded=False):
            self._render_feedback_stats()

    def _render_feedback_form(self):
        """Render the main feedback form"""
        st.write("**Help us improve this medical AI platform!**")
        
        # User type selection
        user_type = st.selectbox(
            "I am a:",
            ["Student", "Researcher", "Healthcare Professional", "Data Scientist", 
             "Educator/Teacher", "Industry Professional", "Other"],
            key="feedback_user_type"
        )

        # Experience level
        experience = st.select_slider(
            "Your ML/AI experience level:",
            options=["Beginner", "Intermediate", "Advanced", "Expert"],
            value="Intermediate",
            key="feedback_experience"
        )

        # Overall rating
        rating = st.select_slider(
            "Overall rating of this platform:",
            options=["⭐ Poor", "⭐⭐ Fair", "⭐⭐⭐ Good", "⭐⭐⭐⭐ Very Good", "⭐⭐⭐⭐⭐ Excellent"],
            value="⭐⭐⭐ Good",
            key="feedback_rating"
        )

        # Specific feature ratings
        st.write("**Rate specific features:**")
        
        col1, col2 = st.columns(2)
        with col1:
            ml_models_rating = st.slider("ML Models", 1, 5, 3, key="ml_models_rating")
            data_quality_rating = st.slider("Data Quality", 1, 5, 4, key="data_quality_rating")
        
        with col2:
            ui_rating = st.slider("User Interface", 1, 5, 3, key="ui_rating")
            docs_rating = st.slider("Documentation", 1, 5, 3, key="docs_rating")

        # Usage frequency
        usage_frequency = st.radio(
            "How often do you plan to use this platform?",
            ["First time visit", "Occasionally", "Weekly", "Daily", "For a specific project"],
            key="feedback_usage_frequency"
        )

        # Most valuable feature
        valuable_feature = st.multiselect(
            "Most valuable features (select all that apply):",
            ["Risk Prediction Model", "Patient Clustering", "Code Examples", 
             "Synthetic Data", "Educational Content", "Analytics Dashboard",
             "Open Source Access"],
            key="feedback_valuable_features"
        )

        # Improvement suggestions
        improvement_area = st.multiselect(
            "Areas for improvement (select all that apply):",
            ["More ML Models", "Better Documentation", "More Data Features",
             "Performance Optimization", "Additional Tutorials", "Mobile Support",
             "API Access", "Export Features"],
            key="feedback_improvements"
        )

        # Detailed feedback
        feedback_text = st.text_area(
            "Detailed feedback or suggestions:",
            placeholder="Tell us about your experience, suggestions for improvement, or any issues you encountered...",
            height=100,
            key="feedback_text"
        )

        # Optional email for follow-up
        email = st.text_input(
            "📧 Email (optional - for follow-up or updates):",
            placeholder="your.email@example.com",
            key="feedback_email"
        )

        # Submit feedback
        col1, col2 = st.columns([1, 1])
        with col1:
            submit_feedback = st.button("🚀 Submit Feedback", use_container_width=True)
        with col2:
            clear_form = st.button("🗑️ Clear Form", use_container_width=True)

        if clear_form:
            # Clear all form fields
            for key in st.session_state.keys():
                if key.startswith('feedback_'):
                    del st.session_state[key]
            st.rerun()

        if submit_feedback:
            # Validate email if provided
            if email and not self.validate_email(email):
                st.error("❌ Please enter a valid email address or leave it empty.")
                return

            # Prepare feedback data
            feedback_data = {
                "feedback_id": str(uuid.uuid4()),
                "timestamp": datetime.datetime.now().isoformat(),
                "user_type": user_type,
                "experience_level": experience,
                "overall_rating": rating,
                "feature_ratings": {
                    "ml_models": ml_models_rating,
                    "data_quality": data_quality_rating,
                    "ui": ui_rating,
                    "documentation": docs_rating
                },
                "usage_frequency": usage_frequency,
                "valuable_features": valuable_feature,
                "improvement_areas": improvement_area,
                "feedback_text": feedback_text,
                "email": email if email and self.validate_email(email) else None,
                "session_id": st.session_state.get('session_id', 'unknown'),
                "user_agent": st.session_state.get('user_agent', 'unknown')
            }

            success = self.save_feedback(feedback_data)
            if success:
                st.success("✅ Thank you for your detailed feedback!")
                if email:
                    st.info("📧 We'll keep you updated on improvements!")
                
                # Add Google Analytics event tracking
                try:
                    from google_analytics_integration import track_event
                    track_event('feedback_submitted',
                               event_category='User_Engagement',
                               event_label=f'{user_type} - {rating}')
                except:
                    pass

                # Clear form after successful submission
                for key in st.session_state.keys():
                    if key.startswith('feedback_'):
                        del st.session_state[key]
                st.rerun()

    def _render_contact_form(self):
        """Render newsletter and contact form"""
        st.write("**Join our community & get updates!**")
        
        name = st.text_input("Name:", placeholder="Your name", key="contact_name")
        email = st.text_input("Email:", placeholder="your.email@example.com", key="contact_email")
        
        interests = st.multiselect(
            "Interested in:",
            ["Medical AI Updates", "New Features", "Research Collaborations", 
             "Educational Content", "Open Source Contributions"],
            key="contact_interests"
        )
        
        newsletter = st.checkbox(
            "📰 Subscribe to newsletter (monthly updates on medical AI advances)",
            key="contact_newsletter"
        )
        
        research_collaboration = st.checkbox(
            "🔬 Interested in research collaborations",
            key="contact_research"
        )
        
        message = st.text_area(
            "Message (optional):",
            placeholder="Any specific interests or collaboration ideas...",
            height=80,
            key="contact_message"
        )

        if st.button("💌 Join Community", use_container_width=True):
            if not email or not self.validate_email(email):
                st.error("❌ Please enter a valid email address.")
                return
            
            if not name.strip():
                st.error("❌ Please enter your name.")
                return

            contact_data = {
                "contact_id": str(uuid.uuid4()),
                "timestamp": datetime.datetime.now().isoformat(),
                "name": name.strip(),
                "email": email.strip().lower(),
                "interests": interests,
                "newsletter_subscription": newsletter,
                "research_collaboration": research_collaboration,
                "message": message.strip() if message else None,
                "session_id": st.session_state.get('session_id', 'unknown'),
                "source": "medical_ai_demo"
            }

            success = self.save_contact(contact_data)
            if success:
                st.success("✅ Welcome to our community!")
                if newsletter:
                    st.info("📰 You'll receive our monthly newsletter with the latest medical AI advances!")
                
                # Clear contact form
                for key in st.session_state.keys():
                    if key.startswith('contact_'):
                        del st.session_state[key]
                st.rerun()

    def _render_feedback_stats(self):
        """Render feedback statistics"""
        try:
            stats = self.get_feedback_stats()
            
            st.metric("Total Feedback", stats['total_feedback'])
            if stats['total_feedback'] > 0:
                st.metric("Average Rating", f"{stats['average_rating']:.1f}/5.0 ⭐")
            
            # Recent feedback trends
            if stats['total_feedback'] > 0:
                recent_feedback = self.get_recent_feedback(limit=5)
                if recent_feedback:
                    st.write("**Recent Feedback:**")
                    for feedback in recent_feedback:
                        rating_stars = "⭐" * len([c for c in feedback['overall_rating'] if c == '⭐'])
                        st.write(f"• {rating_stars} - {feedback['user_type']} ({feedback['timestamp'][:10]})")
            
        except Exception as e:
            st.write("📊 Feedback stats loading...")

    def save_feedback(self, feedback_data: Dict) -> bool:
        """Save feedback to JSON file with enhanced error handling"""
        try:
            # Load existing data
            with open(self.feedback_file, 'r') as f:
                data = json.load(f)
            
            # Add new feedback
            data["feedback"].append(feedback_data)
            
            # Update stats
            data["stats"]["total_feedback"] = len(data["feedback"])
            ratings = []
            for fb in data["feedback"]:
                rating_text = fb.get("overall_rating", "")
                rating_num = len([c for c in rating_text if c == '⭐'])
                if rating_num > 0:
                    ratings.append(rating_num)
            
            if ratings:
                data["stats"]["average_rating"] = sum(ratings) / len(ratings)
            data["stats"]["last_updated"] = datetime.datetime.now().isoformat()
            
            # Save updated data
            with open(self.feedback_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        
        except Exception as e:
            st.error(f"Error saving feedback: {str(e)}")
            return False

    def save_contact(self, contact_data: Dict) -> bool:
        """Save contact information"""
        try:
            # Load existing contacts
            with open(self.contact_file, 'r') as f:
                data = json.load(f)
            
            # Check for duplicate email
            existing_emails = [contact['email'] for contact in data["contacts"]]
            if contact_data['email'] in existing_emails:
                st.warning("📧 This email is already in our system. Thank you!")
                return True
            
            # Add new contact
            data["contacts"].append(contact_data)
            
            # Add to newsletter if subscribed
            if contact_data['newsletter_subscription']:
                data["newsletter_subscribers"].append({
                    "email": contact_data['email'],
                    "name": contact_data['name'],
                    "timestamp": contact_data['timestamp'],
                    "interests": contact_data['interests']
                })
            
            # Update stats
            data["stats"]["total_contacts"] = len(data["contacts"])
            data["stats"]["newsletter_subscribers"] = len(data["newsletter_subscribers"])
            data["stats"]["last_updated"] = datetime.datetime.now().isoformat()
            
            # Save updated data
            with open(self.contact_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            return True
        
        except Exception as e:
            st.error(f"Error saving contact: {str(e)}")
            return False

    def get_feedback_stats(self) -> Dict:
        """Get feedback statistics"""
        try:
            with open(self.feedback_file, 'r') as f:
                data = json.load(f)
            return data.get("stats", {"total_feedback": 0, "average_rating": 0})
        except:
            return {"total_feedback": 0, "average_rating": 0}

    def get_recent_feedback(self, limit: int = 10) -> List[Dict]:
        """Get recent feedback entries"""
        try:
            with open(self.feedback_file, 'r') as f:
                data = json.load(f)
            
            feedback_list = data.get("feedback", [])
            # Sort by timestamp (newest first) and limit
            sorted_feedback = sorted(feedback_list, 
                                   key=lambda x: x.get("timestamp", ""), 
                                   reverse=True)
            return sorted_feedback[:limit]
        except:
            return []

    def get_contact_stats(self) -> Dict:
        """Get contact and newsletter statistics"""
        try:
            with open(self.contact_file, 'r') as f:
                data = json.load(f)
            return data.get("stats", {"total_contacts": 0, "newsletter_subscribers": 0})
        except:
            return {"total_contacts": 0, "newsletter_subscribers": 0}

    def export_feedback_data(self) -> pd.DataFrame:
        """Export feedback data as pandas DataFrame"""
        try:
            with open(self.feedback_file, 'r') as f:
                data = json.load(f)
            
            feedback_list = data.get("feedback", [])
            if not feedback_list:
                return pd.DataFrame()
            
            # Flatten the data for DataFrame
            flattened_data = []
            for fb in feedback_list:
                flat_fb = {
                    'timestamp': fb.get('timestamp'),
                    'user_type': fb.get('user_type'),
                    'experience_level': fb.get('experience_level'),
                    'overall_rating': fb.get('overall_rating'),
                    'usage_frequency': fb.get('usage_frequency'),
                    'feedback_text': fb.get('feedback_text'),
                    'email_provided': bool(fb.get('email')),
                    'valuable_features': ', '.join(fb.get('valuable_features', [])),
                    'improvement_areas': ', '.join(fb.get('improvement_areas', []))
                }
                
                # Add feature ratings
                feature_ratings = fb.get('feature_ratings', {})
                flat_fb.update({
                    f'{key}_rating': value 
                    for key, value in feature_ratings.items()
                })
                
                flattened_data.append(flat_fb)
            
            return pd.DataFrame(flattened_data)
        
        except Exception as e:
            st.error(f"Error exporting feedback data: {str(e)}")
            return pd.DataFrame()

    def export_contacts_data(self) -> pd.DataFrame:
        """Export contact data as pandas DataFrame"""
        try:
            with open(self.contact_file, 'r') as f:
                data = json.load(f)
            
            contacts_list = data.get("contacts", [])
            if not contacts_list:
                return pd.DataFrame()
            
            # Process contacts data
            for contact in contacts_list:
                contact['interests'] = ', '.join(contact.get('interests', []))
            
            return pd.DataFrame(contacts_list)
        
        except Exception as e:
            st.error(f"Error exporting contact data: {str(e)}")
            return pd.DataFrame()

# Initialize global enhanced feedback collector
if 'enhanced_feedback_collector' not in st.session_state:
    st.session_state.enhanced_feedback_collector = EnhancedFeedbackCollector()
