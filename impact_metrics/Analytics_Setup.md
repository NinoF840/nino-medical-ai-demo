# Analytics Setup and Baseline Metrics

## Current Analytics Infrastructure

### GitHub Analytics (Built-in)
- **Repository Stats**: Stars, forks, watchers, contributors
- **Traffic Analytics**: Views, unique visitors, clones
- **Community Metrics**: Issues, pull requests, discussions
- **Code Analytics**: Commits, code frequency, contributors

### Streamlit Analytics Implementation
```python
# analytics_tracker.py
import streamlit as st
import datetime
import json
import os

class AnalyticsTracker:
    def __init__(self):
        self.analytics_file = "analytics/usage_data.json"
        self.ensure_analytics_dir()
    
    def ensure_analytics_dir(self):
        os.makedirs("analytics", exist_ok=True)
        if not os.path.exists(self.analytics_file):
            with open(self.analytics_file, 'w') as f:
                json.dump({"sessions": [], "features": {}}, f)
    
    def track_session(self, user_id=None):
        """Track user session"""
        session_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user_id": user_id or st.session_state.get('user_id', 'anonymous'),
            "session_id": st.session_state.get('session_id', 'unknown')
        }
        
        with open(self.analytics_file, 'r') as f:
            data = json.load(f)
        
        data["sessions"].append(session_data)
        
        with open(self.analytics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def track_feature_usage(self, feature_name):
        """Track feature usage"""
        with open(self.analytics_file, 'r') as f:
            data = json.load(f)
        
        if feature_name not in data["features"]:
            data["features"][feature_name] = 0
        
        data["features"][feature_name] += 1
        
        with open(self.analytics_file, 'w') as f:
            json.dump(data, f, indent=2)
    
    def get_analytics_summary(self):
        """Get analytics summary"""
        with open(self.analytics_file, 'r') as f:
            data = json.load(f)
        
        return {
            "total_sessions": len(data["sessions"]),
            "unique_users": len(set(s.get("user_id", "anonymous") for s in data["sessions"])),
            "feature_usage": data["features"],
            "last_30_days": self._get_recent_sessions(30)
        }
    
    def _get_recent_sessions(self, days):
        """Get sessions from last N days"""
        cutoff = datetime.datetime.now() - datetime.timedelta(days=days)
        
        with open(self.analytics_file, 'r') as f:
            data = json.load(f)
        
        recent_sessions = [
            s for s in data["sessions"]
            if datetime.datetime.fromisoformat(s["timestamp"]) > cutoff
        ]
        
        return len(recent_sessions)
```

### User Feedback Collection System
```python
# feedback_collector.py
import streamlit as st
import json
import datetime

def collect_user_feedback():
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
            
            save_feedback(feedback_data)
            st.success("Thank you for your feedback!")

def save_feedback(feedback_data):
    """Save feedback to JSON file"""
    feedback_file = "analytics/feedback.json"
    
    try:
        with open(feedback_file, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {"feedback": []}
    
    data["feedback"].append(feedback_data)
    
    with open(feedback_file, 'w') as f:
        json.dump(data, f, indent=2)
```

## Baseline Metrics Collection

### Current Repository Statistics
```bash
# Script to collect baseline GitHub metrics
echo "=== GitHub Repository Baseline Metrics ===" > baseline_metrics.txt
echo "Date: $(date)" >> baseline_metrics.txt
echo "" >> baseline_metrics.txt

# Get repository stats using GitHub CLI (if available)
if command -v gh &> /dev/null; then
    echo "Repository Statistics:" >> baseline_metrics.txt
    gh repo view --json stargazerCount,forkCount,watcherCount >> baseline_metrics.txt
    echo "" >> baseline_metrics.txt
    
    echo "Recent Activity:" >> baseline_metrics.txt
    gh repo view --json createdAt,updatedAt,pushedAt >> baseline_metrics.txt
    echo "" >> baseline_metrics.txt
fi

# Get file and commit statistics
echo "Code Statistics:" >> baseline_metrics.txt
echo "Total files: $(find . -type f -name "*.py" -o -name "*.md" -o -name "*.txt" | wc -l)" >> baseline_metrics.txt
echo "Python files: $(find . -name "*.py" | wc -l)" >> baseline_metrics.txt
echo "Documentation files: $(find . -name "*.md" | wc -l)" >> baseline_metrics.txt
echo "Total commits: $(git rev-list --all --count)" >> baseline_metrics.txt
echo "Contributors: $(git log --format='%aN' | sort -u | wc -l)" >> baseline_metrics.txt
```

### Survey Templates

#### Educational Usage Survey
```markdown
# Educational Usage Survey

## About You
1. What is your role?
   - [ ] Student (Undergraduate)
   - [ ] Student (Graduate)
   - [ ] Researcher
   - [ ] Educator/Professor
   - [ ] Healthcare Professional
   - [ ] Industry Professional
   - [ ] Other: ___________

2. What is your field of study/work?
   - [ ] Computer Science/AI
   - [ ] Medicine/Healthcare
   - [ ] Biomedical Engineering
   - [ ] Data Science
   - [ ] Other: ___________

## Usage Experience
3. How did you discover this tool?
   - [ ] GitHub search
   - [ ] Academic paper/publication
   - [ ] Social media
   - [ ] Colleague recommendation
   - [ ] Course material
   - [ ] Other: ___________

4. How are you using this tool?
   - [ ] Learning AI/ML concepts
   - [ ] Understanding medical AI
   - [ ] Course assignment/project
   - [ ] Research project
   - [ ] Teaching material
   - [ ] Other: ___________

5. How useful is this tool for your needs? (1-5 scale)
   - [ ] 1 - Not useful
   - [ ] 2 - Slightly useful
   - [ ] 3 - Moderately useful
   - [ ] 4 - Very useful
   - [ ] 5 - Extremely useful

## Feedback
6. What features do you find most valuable?
   ___________________________________________

7. What improvements would you suggest?
   ___________________________________________

8. Would you recommend this tool to others?
   - [ ] Yes, definitely
   - [ ] Yes, probably
   - [ ] Maybe
   - [ ] Probably not
   - [ ] Definitely not

## Contact (Optional)
9. Email (for follow-up): ___________
10. Institution: ___________
```

### Implementation Timeline

#### Week 1 (Current)
- [x] Create analytics infrastructure code
- [x] Design feedback collection system
- [x] Prepare survey templates
- [ ] Set up baseline metrics collection

#### Week 2
- [ ] Implement analytics tracking in Streamlit app
- [ ] Deploy feedback collection system
- [ ] Launch first educational usage survey
- [ ] Set up automated metrics collection

#### Week 3
- [ ] Analyze first week of data
- [ ] Refine collection methods
- [ ] Expand survey distribution
- [ ] Create initial dashboard

#### Week 4
- [ ] Prepare first monthly report
- [ ] Identify key trends
- [ ] Optimize tracking systems
- [ ] Plan quarterly report structure

## Data Privacy and Compliance

### GDPR Compliance
- All data collection is opt-in
- Clear privacy notices provided
- Data minimization principles followed
- Right to access and deletion supported
- Anonymous data collection where possible

### Data Storage
- Local file storage initially
- Encrypted storage for sensitive data
- Regular backup procedures
- Access controls implemented
- Retention policies defined

## Contact Information
- **Data Officer**: [To be assigned]
- **Privacy Coordinator**: [To be assigned]
- **Technical Support**: [Technical lead contact]
