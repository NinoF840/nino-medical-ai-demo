import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import os
from enhanced_feedback_collector import EnhancedFeedbackCollector

# Page configuration
st.set_page_config(
    page_title="Feedback Dashboard - Nino Medical AI",
    page_icon="📊",
    layout="wide"
)

def create_feedback_dashboard():
    """Create the feedback analytics dashboard"""
    
    # Navigation header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("📊 User Feedback Dashboard")
        st.markdown("**Nino Medical AI Demo - Feedback Analytics**")
    
    with col2:
        if st.button("🏥 Medical AI Demo", use_container_width=True):
            st.switch_page("app.py")
    
    with col3:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.rerun()
    
    st.markdown("---")
    
    # Initialize feedback collector
    feedback_collector = EnhancedFeedbackCollector()
    
    # Check if feedback data exists
    if not os.path.exists(feedback_collector.feedback_file):
        st.warning("No feedback data available yet.")
        return
    
    try:
        # Load feedback data
        with open(feedback_collector.feedback_file, 'r') as f:
            feedback_data = json.load(f)
        
        # Load contact data
        contact_data = {}
        if os.path.exists(feedback_collector.contact_file):
            with open(feedback_collector.contact_file, 'r') as f:
                contact_data = json.load(f)
    
    except Exception as e:
        st.error(f"Error loading feedback data: {str(e)}")
        return
    
    # Key Metrics
    st.header("📈 Key Metrics")
    
    feedback_stats = feedback_data.get("stats", {})
    contact_stats = contact_data.get("stats", {})
    feedback_list = feedback_data.get("feedback", [])
    contacts_list = contact_data.get("contacts", [])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📝 Total Feedback", feedback_stats.get('total_feedback', 0))
    
    with col2:
        avg_rating = feedback_stats.get('average_rating', 0)
        st.metric("⭐ Average Rating", f"{avg_rating:.1f}/5.0")
    
    with col3:
        st.metric("👥 Total Contacts", contact_stats.get('total_contacts', 0))
    
    with col4:
        st.metric("📰 Newsletter Subscribers", contact_stats.get('newsletter_subscribers', 0))
    
    # Recent Activity
    col1, col2 = st.columns(2)
    
    with col1:
        # Recent 7 days feedback
        recent_feedback = 0
        if feedback_list:
            week_ago = datetime.now() - timedelta(days=7)
            for fb in feedback_list:
                try:
                    fb_time = datetime.fromisoformat(fb.get('timestamp', ''))
                    if fb_time > week_ago:
                        recent_feedback += 1
                except:
                    continue
        st.metric("📅 Feedback (Last 7 Days)", recent_feedback)
    
    with col2:
        # Recent 7 days contacts
        recent_contacts = 0
        if contacts_list:
            week_ago = datetime.now() - timedelta(days=7)
            for contact in contacts_list:
                try:
                    contact_time = datetime.fromisoformat(contact.get('timestamp', ''))
                    if contact_time > week_ago:
                        recent_contacts += 1
                except:
                    continue
        st.metric("📧 New Contacts (Last 7 Days)", recent_contacts)
    
    st.markdown("---")
    
    # Feedback Analysis
    if feedback_list:
        st.header("📊 Feedback Analysis")
        
        # Convert to DataFrame for analysis
        feedback_df = pd.DataFrame(feedback_list)
        feedback_df['timestamp'] = pd.to_datetime(feedback_df['timestamp'])
        feedback_df['date'] = feedback_df['timestamp'].dt.date
        
        # Rating Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("⭐ Rating Distribution")
            if 'overall_rating' in feedback_df.columns:
                # Extract numeric ratings
                feedback_df['rating_numeric'] = feedback_df['overall_rating'].apply(
                    lambda x: len([c for c in str(x) if c == '⭐']) if pd.notna(x) else 0
                )
                
                rating_counts = feedback_df['rating_numeric'].value_counts().sort_index()
                rating_labels = [f"{i} Star{'s' if i != 1 else ''}" for i in rating_counts.index]
                
                fig = px.bar(
                    x=rating_labels,
                    y=rating_counts.values,
                    title="Rating Distribution",
                    color=rating_counts.values,
                    color_continuous_scale='RdYlGn'
                )
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("👥 User Types")
            if 'user_type' in feedback_df.columns:
                user_type_counts = feedback_df['user_type'].value_counts()
                
                fig = px.pie(
                    values=user_type_counts.values,
                    names=user_type_counts.index,
                    title="Feedback by User Type"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Feedback Over Time
        st.subheader("📈 Feedback Trends")
        daily_feedback = feedback_df.groupby('date').size().reset_index(name='feedback_count')
        daily_feedback['date'] = pd.to_datetime(daily_feedback['date'])
        
        fig = px.line(
            daily_feedback,
            x='date',
            y='feedback_count',
            title="Daily Feedback Submissions",
            markers=True
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Experience Level Analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🎓 Experience Levels")
            if 'experience_level' in feedback_df.columns:
                exp_counts = feedback_df['experience_level'].value_counts()
                
                fig = px.bar(
                    x=exp_counts.index,
                    y=exp_counts.values,
                    title="Users by Experience Level"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("🔄 Usage Frequency")
            if 'usage_frequency' in feedback_df.columns:
                usage_counts = feedback_df['usage_frequency'].value_counts()
                
                fig = px.bar(
                    x=usage_counts.values,
                    y=usage_counts.index,
                    orientation='h',
                    title="Planned Usage Frequency"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Feature Ratings Analysis
        st.subheader("🔧 Feature Ratings Analysis")
        
        feature_ratings_data = []
        for fb in feedback_list:
            ratings = fb.get('feature_ratings', {})
            for feature, rating in ratings.items():
                feature_ratings_data.append({
                    'feature': feature.replace('_', ' ').title(),
                    'rating': rating,
                    'timestamp': fb.get('timestamp')
                })
        
        if feature_ratings_data:
            features_df = pd.DataFrame(feature_ratings_data)
            avg_feature_ratings = features_df.groupby('feature')['rating'].mean().sort_values(ascending=True)
            
            fig = px.bar(
                x=avg_feature_ratings.values,
                y=avg_feature_ratings.index,
                orientation='h',
                title="Average Feature Ratings",
                color=avg_feature_ratings.values,
                color_continuous_scale='RdYlGn'
            )
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        
        # Most Valuable Features
        st.subheader("💎 Most Valuable Features")
        
        all_valuable_features = []
        for fb in feedback_list:
            valuable_features = fb.get('valuable_features', [])
            all_valuable_features.extend(valuable_features)
        
        if all_valuable_features:
            valuable_counts = pd.Series(all_valuable_features).value_counts()
            
            fig = px.bar(
                x=valuable_counts.values,
                y=valuable_counts.index,
                orientation='h',
                title="Features Rated as Most Valuable"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Improvement Areas
        st.subheader("🔧 Requested Improvements")
        
        all_improvements = []
        for fb in feedback_list:
            improvements = fb.get('improvement_areas', [])
            all_improvements.extend(improvements)
        
        if all_improvements:
            improvement_counts = pd.Series(all_improvements).value_counts()
            
            fig = px.bar(
                x=improvement_counts.values,
                y=improvement_counts.index,
                orientation='h',
                title="Most Requested Improvements"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Contact Analysis
    if contacts_list:
        st.header("📧 Contact & Newsletter Analysis")
        
        contacts_df = pd.DataFrame(contacts_list)
        contacts_df['timestamp'] = pd.to_datetime(contacts_df['timestamp'])
        contacts_df['date'] = contacts_df['timestamp'].dt.date
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Contact Registrations")
            daily_contacts = contacts_df.groupby('date').size().reset_index(name='contact_count')
            daily_contacts['date'] = pd.to_datetime(daily_contacts['date'])
            
            fig = px.line(
                daily_contacts,
                x='date',
                y='contact_count',
                title="Daily Contact Registrations",
                markers=True
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📰 Newsletter vs Contacts")
            newsletter_stats = {
                'Newsletter Subscribers': len([c for c in contacts_list if c.get('newsletter_subscription', False)]),
                'General Contacts': len([c for c in contacts_list if not c.get('newsletter_subscription', False)])
            }
            
            fig = px.pie(
                values=list(newsletter_stats.values()),
                names=list(newsletter_stats.keys()),
                title="Newsletter Subscription Rate"
            )
            st.plotly_chart(fig, use_container_width=True)
        
        # Interest Analysis
        st.subheader("🎯 Interest Areas")
        
        all_interests = []
        for contact in contacts_list:
            interests = contact.get('interests', [])
            all_interests.extend(interests)
        
        if all_interests:
            interest_counts = pd.Series(all_interests).value_counts()
            
            fig = px.bar(
                x=interest_counts.values,
                y=interest_counts.index,
                orientation='h',
                title="Most Popular Interest Areas"
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Recent Feedback Table
    st.header("📝 Recent Feedback Details")
    
    if feedback_list:
        recent_feedback = sorted(feedback_list, key=lambda x: x.get('timestamp', ''), reverse=True)[:10]
        
        display_feedback = []
        for fb in recent_feedback:
            display_feedback.append({
                'Date': fb.get('timestamp', '')[:10],
                'User Type': fb.get('user_type', 'Unknown'),
                'Rating': fb.get('overall_rating', ''),
                'Experience': fb.get('experience_level', ''),
                'Email Provided': '✅' if fb.get('email') else '❌',
                'Feedback Preview': (fb.get('feedback_text', '') or 'No text')[:100] + '...' if len(fb.get('feedback_text', '')) > 100 else fb.get('feedback_text', 'No text')
            })
        
        feedback_table_df = pd.DataFrame(display_feedback)
        st.dataframe(feedback_table_df, use_container_width=True)
    
    # Export Functionality
    st.header("📤 Export Data")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📊 Export Feedback CSV"):
            try:
                feedback_export_df = feedback_collector.export_feedback_data()
                if not feedback_export_df.empty:
                    csv_data = feedback_export_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download Feedback CSV",
                        data=csv_data,
                        file_name=f"feedback_data_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No feedback data to export")
            except Exception as e:
                st.error(f"Error exporting feedback: {str(e)}")
    
    with col2:
        if st.button("📧 Export Contacts CSV"):
            try:
                contacts_export_df = feedback_collector.export_contacts_data()
                if not contacts_export_df.empty:
                    csv_data = contacts_export_df.to_csv(index=False)
                    st.download_button(
                        label="💾 Download Contacts CSV",
                        data=csv_data,
                        file_name=f"contacts_data_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("No contact data to export")
            except Exception as e:
                st.error(f"Error exporting contacts: {str(e)}")
    
    with col3:
        if st.button("📋 Generate Summary Report"):
            # Generate comprehensive report
            report = f"""
# Feedback & Contact Summary Report
**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Feedback Statistics
- Total Feedback Submissions: {feedback_stats.get('total_feedback', 0)}
- Average Rating: {feedback_stats.get('average_rating', 0):.1f}/5.0
- Recent Feedback (7 days): {recent_feedback}

## Contact Statistics  
- Total Contacts: {contact_stats.get('total_contacts', 0)}
- Newsletter Subscribers: {contact_stats.get('newsletter_subscribers', 0)}
- Recent Contacts (7 days): {recent_contacts}

## Top User Insights
"""
            
            if feedback_list:
                # Add top user type
                user_types = pd.Series([fb.get('user_type') for fb in feedback_list]).value_counts()
                if not user_types.empty:
                    report += f"- Most Active User Type: {user_types.index[0]} ({user_types.iloc[0]} submissions)\n"
                
                # Add most valuable feature
                all_valuable = []
                for fb in feedback_list:
                    all_valuable.extend(fb.get('valuable_features', []))
                if all_valuable:
                    valuable_counts = pd.Series(all_valuable).value_counts()
                    report += f"- Most Valued Feature: {valuable_counts.index[0]} ({valuable_counts.iloc[0]} votes)\n"
            
            report += f"""

## Recent Activity Trends
- Feedback activity is {'increasing' if recent_feedback > 0 else 'stable'}
- Contact registrations are {'growing' if recent_contacts > 0 else 'stable'}

---
*This report was generated automatically by the Nino Medical AI Feedback System*
"""
            
            st.download_button(
                label="💾 Download Report",
                data=report,
                file_name=f"feedback_summary_{datetime.now().strftime('%Y%m%d')}.txt",
                mime="text/plain"
            )

if __name__ == "__main__":
    create_feedback_dashboard()
