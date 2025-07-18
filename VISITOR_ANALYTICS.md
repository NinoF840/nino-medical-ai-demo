# 📊 Visitor Analytics Dashboard

The **Visitor Analytics Dashboard** is a comprehensive analytics system for tracking and analyzing user interactions with the Nino Medical AI Demo. It provides real-time insights into user behavior, feature usage, and engagement patterns.

## 🚀 Quick Start

### Running the Analytics Dashboard

```bash
# Option 1: Run only the analytics dashboard
python run_demo.py --analytics

# Option 2: Run both main app and analytics (recommended)
python run_demo.py --both

# Option 3: Run with automatic browser opening
python run_demo.py --both --browser

# Option 4: Run individual components
streamlit run visitor_dashboard.py --server.port 8502
```

### Accessing the Dashboard

- **Analytics Dashboard**: http://localhost:8502
- **Main Medical AI Demo**: http://localhost:8501

## 📋 Features

### 🎯 Key Metrics
- **Total Sessions**: Count of all user sessions
- **Unique Users**: Number of distinct visitors
- **Recent Activity**: Sessions in the last 7 days and today
- **Active Users**: Real-time active user estimation

### 📈 Visualizations
- **Daily Visits Chart**: Line chart showing visit trends over time
- **Hourly Distribution**: Bar chart of peak usage hours
- **Feature Usage**: Most popular features and their usage counts
- **Geographic Analytics**: Visitor locations by country and city
- **Browser Analysis**: Distribution of browsers used by visitors

### 🔔 Real-Time Notifications
- New visitor alerts with geographic information
- Feature usage milestones
- Daily summary notifications
- System status updates

### 📊 Performance Insights
- Peak usage patterns
- Most active days
- Popular features analysis
- User engagement trends

### 📤 Export Capabilities
- **CSV Export**: Download session data for external analysis
- **Report Generation**: Comprehensive analytics reports
- **Email Integration**: (Template for production deployment)

## 🏗️ Architecture

### Analytics Components

```
nino-medical-ai-demo/
├── visitor_dashboard.py          # Main dashboard UI
├── analytics_tracker.py          # Basic session tracking
├── enhanced_analytics.py         # Advanced tracking with geolocation
├── notification_manager.py       # Notification system
├── run_demo.py                   # Deployment script
└── analytics/
    ├── usage_data.json           # Session and feature data
    ├── geo_data.json            # Geographic analytics
    └── notifications.json        # Notification history
```

### Data Flow

1. **Session Initialization**: When a user visits the main app
   - Generate unique session ID
   - Track user agent and timestamp
   - Attempt geolocation (if enabled)
   - Store session data

2. **Feature Tracking**: When users interact with features
   - Record feature usage
   - Update usage counters
   - Track interaction patterns

3. **Real-Time Analytics**: Dashboard updates
   - Load latest session data
   - Generate insights and metrics
   - Display visualizations
   - Show notifications

## 🛠️ Configuration

### Analytics Settings

You can customize analytics behavior by modifying the tracker classes:

```python
# In analytics_tracker.py
class AnalyticsTracker:
    def __init__(self):
        self.analytics_file = "analytics/usage_data.json"  # Data storage location
        # ... other configuration
```

### Geolocation Settings

```python
# In enhanced_analytics.py
def get_geolocation(self, ip_address):
    # Uses ip-api.com for geolocation (free service)
    # Can be replaced with other services
    response = requests.get(
        f'http://ip-api.com/json/{ip_address}?fields=country,regionName,city,timezone,status',
        timeout=5
    )
```

## 📊 Data Structure

### Session Data Format
```json
{
  "sessions": [
    {
      "timestamp": "2025-01-19T10:30:00",
      "user_id": "anonymous",
      "session_id": "abc123...",
      "user_agent": "Mozilla/5.0...",
      "ip_address": "192.168.1.1",
      "geo_data": {
        "country": "Italy",
        "region": "Lazio",
        "city": "Rome",
        "timezone": "Europe/Rome"
      }
    }
  ],
  "features": {
    "model_training_process": 15,
    "clustering_analysis": 8,
    "ml_code_examples": 12
  },
  "notifications": [
    {
      "timestamp": "2025-01-19T10:30:00",
      "type": "new_visitor",
      "message": "🌍 Nuovo visitatore da Rome, Italy"
    }
  ]
}
```

## 🔧 Customization

### Adding Custom Metrics

1. **Track New Features**:
```python
# In your Streamlit app
st.session_state.analytics_tracker.track_feature_usage("new_feature_name")
```

2. **Custom Notifications**:
```python
# In enhanced_analytics.py
def send_custom_notification(self, message, data=None):
    notification = {
        "timestamp": datetime.datetime.now().isoformat(),
        "type": "custom",
        "message": message,
        "data": data or {}
    }
    # Save notification logic...
```

3. **Additional Visualizations**:
```python
# In visitor_dashboard.py
def create_custom_chart(data):
    fig = px.scatter(data, x='x_column', y='y_column')
    st.plotly_chart(fig, use_container_width=True)
```

### Styling and Branding

The dashboard uses Streamlit's theming system. You can customize:

- Colors and fonts via Streamlit config
- Layout and component arrangement
- Chart styling with Plotly themes
- Custom CSS via `st.markdown()` with `unsafe_allow_html=True`

## 🔒 Privacy & Security

### Data Protection
- **Anonymous Tracking**: No personal information stored
- **IP Address Handling**: Only used for geolocation, then anonymized
- **Local Storage**: All data stored locally, not transmitted externally
- **GDPR Compliance**: Designed with privacy regulations in mind

### Geolocation
- Uses free, public IP geolocation services
- No personal location data stored
- Can be disabled by removing enhanced analytics

### Security Considerations
- No sensitive medical data tracked
- Session IDs are random UUIDs
- Local file storage only
- No external data transmission

## 🚀 Deployment

### Development
```bash
# Run both applications
python run_demo.py --both --browser
```

### Production Considerations

1. **Database Storage**: Replace JSON files with a proper database
2. **Authentication**: Add user authentication for dashboard access
3. **Email Notifications**: Implement SMTP configuration
4. **Monitoring**: Add system health checks
5. **Backup**: Regular data backup procedures

### Docker Deployment
```dockerfile
# Example Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8501 8502

CMD ["python", "run_demo.py", "--both"]
```

## 📈 Analytics Insights

### Interpreting Data

- **Peak Hours**: Identify when your application is most used
- **Feature Popularity**: Focus development on popular features
- **Geographic Reach**: Understand your audience distribution
- **Session Patterns**: Optimize user experience based on usage

### Performance Monitoring

- Monitor session duration trends
- Track feature adoption rates
- Identify usage bottlenecks
- Measure user engagement

## 🤝 Contributing

To enhance the analytics dashboard:

1. **Fork the repository**
2. **Create feature branch**: `git checkout -b feature/new-analytics`
3. **Add your enhancements**
4. **Test thoroughly**
5. **Submit pull request**

### Development Guidelines

- Follow existing code patterns
- Add comprehensive docstrings
- Include error handling
- Test with sample data
- Update documentation

## 📞 Support

For questions about the visitor analytics dashboard:

- **GitHub Issues**: Report bugs or request features
- **GitHub Discussions**: Community support and ideas
- **Email**: nino58150@gmail.com for direct support

## 📄 License

The Visitor Analytics Dashboard is part of the Nino Medical AI Demo and is released under the same open-source license.

---

**Made with ❤️ by the Nino Medical AI Team**

*Empowering medical AI education through comprehensive analytics and insights.*
