# Nino Medical AI Demo - Open Source Platform
import streamlit as st
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Nino Medical AI Demo",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and header
st.title("🏥 Nino Medical AI Platform - Demo")
st.markdown("### Open-source medical AI platform for education and research")

# Important disclaimer
st.error("⚠️ **IMPORTANT DISCLAIMER**: This software is for educational and research purposes only. NOT FOR CLINICAL OR DIAGNOSTIC USE.")

# Welcome section
st.header("👋 Welcome!")
st.write("""This is a demo application showcasing the capabilities of our medical AI platform. 
**All data here is synthetic** - no real patient information is used.""")

# Repository information
st.info("🔗 **Open Source**: Visit our [GitHub Repository](https://github.com/NinoF840/nino-medical-ai-demo) to contribute!")

# Simulated data display
data = {
    "Patient ID": ["001", "002", "003"],
    "Heart Rate": [72, 85, 90],
    "Blood Pressure": ["120/80", "125/85", "130/85"],
    "Condition": ["Stable", "Monitored", "Monitored"]
}

st.subheader("📊 Patient Data")

# Create a proper DataFrame for better display
df = pd.DataFrame(data)
st.dataframe(df, use_container_width=True)

# Add some metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Patients", len(df))
with col2:
    st.metric("Avg Heart Rate", f"{df['Heart Rate'].mean():.0f} bpm")
with col3:
    stable_count = (df['Condition'] == 'Stable').sum()
    st.metric("Stable Patients", stable_count)

# Simulated analysis outcome
st.subheader("🧪 Analysis")
st.success("✅ All parameters are within the normal range. No immediate action required.")

# Add a chart
st.subheader("📈 Heart Rate Visualization")
st.bar_chart(df.set_index('Patient ID')['Heart Rate'])

# Sidebar with additional info
with st.sidebar:
    st.header("📚 About This Demo")
    st.write("""
    This medical AI demo showcases:
    - 🔬 **Synthetic Data Only**
    - ✅ **AI Act Compliant**
    - 💪 **GDPR Compliant**
    - 📝 **Open Source**
    - 🔬 **Research Ready**
    """)
    
    st.header("🔗 Links")
    st.markdown("""
    - [GitHub Repository](https://github.com/NinoF840/nino-medical-ai-demo)
    - [Documentation](https://github.com/NinoF840/nino-medical-ai-demo/blob/main/README.md)
    - [License](https://github.com/NinoF840/nino-medical-ai-demo/blob/main/LICENSE)
    """)

# Integration Guide
st.subheader("🛠️ Integration Guide")
st.write("Learn more about how to integrate with our medical AI API.")

with st.expander("View Integration Example"):
    st.code("""
    # Example integration code
    import requests
    
    # This is a demo - not a real API
    response = requests.get('https://api.nino-medical-ai.demo/analyze')
    data = response.json()
    print(data)
    """, language="python")

# Contact information
st.subheader("📞 Contact Us")
st.write("For more information, partnerships, or security issues, please reach out:")
st.write("📧 **Email**: nino58150@gmail.com")
st.write("👥 **Community**: [GitHub Discussions](https://github.com/NinoF840/nino-medical-ai-demo/discussions)")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    © 2025 Nino Medical AI Demo | Open Source | Educational Use Only
</div>
""", unsafe_allow_html=True)
