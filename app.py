# Nino Medical AI Demo - Open Source Platform
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Import analytics and feedback systems
from analytics_tracker import AnalyticsTracker
from feedback_collector import FeedbackCollector

# Page configuration
st.set_page_config(
    page_title="Nino Medical AI Demo",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Initialize analytics and feedback systems
if 'analytics_tracker' not in st.session_state:
    st.session_state.analytics_tracker = AnalyticsTracker()
if 'feedback_collector' not in st.session_state:
    st.session_state.feedback_collector = FeedbackCollector()

# Title and header
st.title("🏥 Nino Medical AI Demo")
st.markdown("### Open-source educational platform for medical AI learning")

# Important disclaimer
st.error(
    "⚠️ **IMPORTANT DISCLAIMER**: This software is for educational and research purposes only. NOT FOR CLINICAL OR DIAGNOSTIC USE."
)

# Welcome section
st.header("👋 Welcome!")
st.write(
    """This is a demo application showcasing the capabilities of our medical AI platform. 
**All data here is synthetic** - no real patient information is used."""
)

# Repository information
st.info(
    "🔗 **Open Source**: Visit our [GitHub Repository](https://github.com/NinoF840/nino-medical-ai-demo) to contribute!"
)


# Generate synthetic medical data for ML demonstration
@st.cache_data
def generate_synthetic_data(n_patients=100):
    """Generate synthetic medical data for educational purposes."""
    np.random.seed(42)  # For reproducible results

    data = {
        "Patient_ID": [f"P{i:03d}" for i in range(1, n_patients + 1)],
        "Age": np.random.randint(18, 85, n_patients),
        "Heart_Rate": np.random.normal(75, 12, n_patients).astype(int),
        "Systolic_BP": np.random.normal(120, 15, n_patients).astype(int),
        "Diastolic_BP": np.random.normal(80, 10, n_patients).astype(int),
        "Temperature": np.random.normal(98.6, 1.2, n_patients).round(1),
        "Blood_Sugar": np.random.normal(100, 20, n_patients).astype(int),
    }

    # Create risk categories based on multiple factors
    risk_scores = []
    for i in range(n_patients):
        score = 0
        if data["Age"][i] > 65:
            score += 2
        if data["Heart_Rate"][i] > 100 or data["Heart_Rate"][i] < 60:
            score += 1
        if data["Systolic_BP"][i] > 140:
            score += 2
        if data["Diastolic_BP"][i] > 90:
            score += 1
        if data["Blood_Sugar"][i] > 126:
            score += 1
        risk_scores.append(score)

    # Convert scores to categories
    conditions = []
    for score in risk_scores:
        if score <= 1:
            conditions.append("Low Risk")
        elif score <= 3:
            conditions.append("Medium Risk")
        else:
            conditions.append("High Risk")

    data["Risk_Category"] = conditions
    data["Risk_Score"] = risk_scores

    return pd.DataFrame(data)


# Generate the dataset
df = generate_synthetic_data()

st.subheader("📊 Synthetic Patient Dataset")
st.write(f"**Dataset size:** {len(df)} patients | **Features:** {len(df.columns)-2} clinical measurements")

# Display sample of the data
st.dataframe(df.head(10), use_container_width=True)

# Add key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total Patients", len(df))
with col2:
    st.metric("Avg Age", f"{df['Age'].mean():.0f} years")
with col3:
    st.metric("Avg Heart Rate", f"{df['Heart_Rate'].mean():.0f} bpm")
with col4:
    high_risk_count = (df["Risk_Category"] == "High Risk").sum()
    st.metric("High Risk Patients", high_risk_count)

# Machine Learning Analysis Section
st.divider()
st.header("🤖 AI-Powered Analysis")

# Risk Distribution
st.subheader("📈 Risk Category Distribution")
risk_counts = df["Risk_Category"].value_counts()
st.bar_chart(risk_counts)

# Correlation Analysis
st.subheader("🔗 Clinical Parameter Correlations")
numeric_cols = ["Age", "Heart_Rate", "Systolic_BP", "Diastolic_BP", "Temperature", "Blood_Sugar"]
corr_matrix = df[numeric_cols].corr()
st.write("**Correlation Matrix:**")
st.dataframe(corr_matrix.style.background_gradient(cmap="coolwarm"), use_container_width=True)

# Machine Learning Model Demo
st.subheader("🤖 Risk Prediction Model")
st.write("**Realistic Medical AI Model:** Using unbalanced data with class weights for optimal clinical performance")

# Show model approach info
st.info(
    "🏥 **Clinical Approach**: This model uses realistic unbalanced data (like real hospitals) "
    "with class weights to improve detection of high-risk patients - a critical requirement in medical AI."
)

with st.expander("🔍 View Model Training Process"):
    # Track feature usage
    st.session_state.analytics_tracker.track_feature_usage("model_training_process")
    # Prepare features for ML
    X = df[numeric_cols]
    y = df["Risk_Category"]

    # Show class distribution
    class_dist = y.value_counts()
    st.write("📊 **Realistic Class Distribution (like real hospitals):**")
    col1, col2, col3 = st.columns(3)
    with col1:
        low_pct = (class_dist.get("Low Risk", 0) / len(y)) * 100
        st.metric("Low Risk", f"{class_dist.get('Low Risk', 0)}", f"{low_pct:.1f}%")
    with col2:
        med_pct = (class_dist.get("Medium Risk", 0) / len(y)) * 100
        st.metric("Medium Risk", f"{class_dist.get('Medium Risk', 0)}", f"{med_pct:.1f}%")
    with col3:
        high_pct = (class_dist.get("High Risk", 0) / len(y)) * 100
        st.metric("High Risk", f"{class_dist.get('High Risk', 0)}", f"{high_pct:.1f}%")

    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # Train Random Forest model with class weights
    st.write("⚖️ **Using Class Weights for Better Medical AI:**")
    st.write("- Automatically balances learning for rare but critical high-risk cases")
    st.write("- Maintains realistic data distribution while improving minority class detection")

    rf_model = RandomForestClassifier(
        n_estimators=100, random_state=42, class_weight="balanced"  # This is the key improvement!
    )
    rf_model.fit(X_train_scaled, y_train)

    # Make predictions
    y_pred = rf_model.predict(X_test_scaled)
    accuracy = accuracy_score(y_test, y_pred)

    # Calculate detailed metrics
    from sklearn.metrics import f1_score

    f1_macro = f1_score(y_test, y_pred, average="macro")
    f1_weighted = f1_score(y_test, y_pred, average="weighted")

    # Display comprehensive results
    st.write("🎯 **Model Performance (Clinically Optimized):**")

    # Main metrics
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    with metric_col1:
        st.metric("Overall Accuracy", f"{accuracy:.1%}")
    with metric_col2:
        st.metric("Macro F1 Score", f"{f1_macro:.1%}")
    with metric_col3:
        st.metric("Weighted F1 Score", f"{f1_weighted:.1%}")

    # Performance interpretation
    if f1_macro >= 0.80:
        st.success("✅ **Excellent Performance**: F1 score > 80% indicates excellent clinical AI performance")
    elif f1_macro >= 0.70:
        st.success("✅ **Good Performance**: F1 score 70-80% indicates good clinical AI performance")
    elif f1_macro >= 0.60:
        st.warning("⚠️ **Fair Performance**: F1 score 60-70% indicates fair clinical AI performance")
    else:
        st.error("❌ **Poor Performance**: F1 score < 60% indicates poor clinical AI performance")

    st.write("📄 **Detailed Classification Report:**")
    st.text(classification_report(y_test, y_pred))

    # Per-class performance analysis
    st.write("🏥 **Clinical Impact Analysis:**")
    f1_per_class = f1_score(y_test, y_pred, average=None)
    unique_classes = sorted(y.unique())

    for i, class_name in enumerate(unique_classes):
        if class_name == "High Risk":
            if f1_per_class[i] >= 0.70:
                st.success(f"🚨 **{class_name}**: {f1_per_class[i]:.1%} F1 - Excellent detection of critical cases")
            elif f1_per_class[i] >= 0.50:
                st.warning(f"🚨 **{class_name}**: {f1_per_class[i]:.1%} F1 - Adequate detection of critical cases")
            else:
                st.error(f"🚨 **{class_name}**: {f1_per_class[i]:.1%} F1 - Poor detection of critical cases")
        else:
            st.write(f"📊 **{class_name}**: {f1_per_class[i]:.1%} F1 score")

    # Feature importance
    feature_importance = pd.DataFrame(
        {"Feature": numeric_cols, "Importance": rf_model.feature_importances_}
    ).sort_values("Importance", ascending=False)

    st.write("🔍 **Most Important Clinical Features:**")
    st.bar_chart(feature_importance.set_index("Feature"))

    # Clinical insights
    top_feature = feature_importance.iloc[0]["Feature"]
    top_importance = feature_importance.iloc[0]["Importance"]
    st.write(
        f"💡 **Key Clinical Insight**: {top_feature} is the most predictive feature ({top_importance:.1%} importance)"
    )

# Clustering Analysis
st.subheader("🔍 Patient Clustering Analysis")
with st.expander("📏 View Clustering Results"):
    # Track feature usage
    st.session_state.analytics_tracker.track_feature_usage("clustering_analysis")
    # Perform K-means clustering
    X_cluster = df[numeric_cols]
    scaler_cluster = StandardScaler()
    X_scaled = scaler_cluster.fit_transform(X_cluster)

    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)

    # Add cluster labels to dataframe
    df_clustered = df.copy()
    df_clustered["Cluster"] = [f"Group {i+1}" for i in clusters]

    # Show cluster statistics
    st.write("📏 **Cluster Distribution:**")
    cluster_counts = df_clustered["Cluster"].value_counts()
    st.bar_chart(cluster_counts)

    # Cluster characteristics
    st.write("📊 **Cluster Characteristics:**")
    cluster_stats = df_clustered.groupby("Cluster")[numeric_cols].mean().round(1)
    st.dataframe(cluster_stats, use_container_width=True)

# Sidebar with additional info
with st.sidebar:
    st.header("📚 About This Demo")
    st.write(
        """
    This medical AI demo showcases:
    - 🔬 **Synthetic Data Only**
    - 🤖 **Machine Learning Models**
    - ✅ **AI Act Compliant**
    - 💪 **GDPR Compliant**
    - 📝 **Open Source**
    - 🔬 **Research Ready**
    """
    )
    
    # Analytics Dashboard Access
    st.header("📊 Analytics")
    if st.button("🔍 View Analytics Dashboard", use_container_width=True):
        st.switch_page("visitor_dashboard.py")
    
    # Show quick analytics summary
    summary = st.session_state.analytics_tracker.get_analytics_summary()
    st.metric("Total Sessions", summary['total_sessions'])
    st.metric("Unique Users", summary['unique_users'])
    st.metric("Last 30 Days", summary['last_30_days'])
    
    # Add feedback collection
    st.session_state.feedback_collector.collect_user_feedback()

    st.header("🤖 ML Features")
    st.write(
        """
    **Clinical AI Models:**
    - 🎯 Risk Prediction (Random Forest + Class Weights)
    - 🔍 Patient Clustering (K-Means)
    - 📈 Feature Correlation Analysis
    - 📊 Statistical Insights
    - ⚖️ Realistic Unbalanced Data
    
    **Synthetic Dataset:**
    - 100 virtual patients
    - 6 clinical parameters
    - 3 risk categories (realistic distribution)
    - Class-weighted learning for clinical accuracy
    """
    )

    st.header("🔗 Links")
    st.markdown(
        """
    - [GitHub Repository](https://github.com/NinoF840/nino-medical-ai-demo)
    - [Documentation](https://github.com/NinoF840/nino-medical-ai-demo/blob/main/README.md)
    - [License](https://github.com/NinoF840/nino-medical-ai-demo/blob/main/LICENSE)
    """
    )

# Educational Resources
st.divider()
st.subheader("📚 Educational Resources")
st.write("Learn about medical AI concepts and machine learning implementations.")

with st.expander("💻 View ML Code Examples"):
    # Track feature usage
    st.session_state.analytics_tracker.track_feature_usage("ml_code_examples")
    st.write("**Example 1: Medical AI with Class Weights (Recommended)**")
    st.code(
        """
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler
    from sklearn.metrics import f1_score, classification_report
    import pandas as pd
    
    # Load realistic medical data (unbalanced like real hospitals)
    df = load_synthetic_data()
    
    # Prepare features and target
    features = ['Age', 'Heart_Rate', 'Systolic_BP', 'Diastolic_BP', 
               'Temperature', 'Blood_Sugar']
    X = df[features]
    y = df['Risk_Category']  # Unbalanced: ~60% Low, ~35% Medium, ~5% High
    
    # Split and scale data (stratified to maintain class distribution)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42, stratify=y
    )
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Use class_weight='balanced' for better medical AI performance
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight='balanced'  # Key for medical AI!
    )
    
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    # Evaluate with medical-relevant metrics
    f1_macro = f1_score(y_test, y_pred, average='macro')
    print(f'Macro F1 Score: {f1_macro:.3f}')
    print(classification_report(y_test, y_pred))
    """,
        language="python",
    )

    st.write("**Why Class Weights Matter in Medical AI:**")
    st.write(
        """
        - **Realistic Data**: Real hospitals have few high-risk patients (~5%)
        - **Critical Detection**: Missing high-risk patients has serious consequences
        - **Class Weights**: Automatically adjust for imbalanced data
        - **Better F1 Scores**: Improves detection of minority classes
        - **Clinical Relevance**: Maintains real-world data distribution
        """
    )

    st.write("**Example 2: Alternative Approaches**")
    st.code(
        """
    # Option 1: Manual class weights
    from sklearn.utils.class_weight import compute_class_weight
    
    classes = np.unique(y_train)
    weights = compute_class_weight('balanced', classes=classes, y=y_train)
    class_weight_dict = dict(zip(classes, weights))
    
    model = RandomForestClassifier(
        class_weight=class_weight_dict
    )
    
    # Option 2: SMOTE for synthetic oversampling
    from imblearn.over_sampling import SMOTE
    
    smote = SMOTE(random_state=42)
    X_train_smote, y_train_smote = smote.fit_resample(X_train, y_train)
    
    # Option 3: Custom sample weights
    from sklearn.utils.class_weight import compute_sample_weight
    
    sample_weights = compute_sample_weight('balanced', y_train)
    model.fit(X_train_scaled, y_train, sample_weight=sample_weights)
    """,
        language="python",
    )

    st.write("**Example 3: Patient Clustering**")
    st.code(
        """
    from sklearn.cluster import KMeans
    from sklearn.preprocessing import StandardScaler
    import matplotlib.pyplot as plt
    
    # Prepare data for clustering
    features = ['Age', 'Heart_Rate', 'Systolic_BP']
    X = df[features]
    
    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # Perform K-means clustering
    kmeans = KMeans(n_clusters=3, random_state=42)
    clusters = kmeans.fit_predict(X_scaled)
    
    # Add cluster labels to dataframe
    df['Cluster'] = clusters
    
    # Analyze cluster characteristics
    cluster_stats = df.groupby('Cluster')[features].mean()
    print(cluster_stats)
    """,
        language="python",
    )

# Contact information
st.subheader("📞 Contact & Community")
st.write("For educational collaborations, research partnerships, or security issues:")
st.write("📧 **Email**: nino58150@gmail.com")
st.write("👥 **Community**: [GitHub Discussions](https://github.com/NinoF840/nino-medical-ai-demo/discussions)")
st.write("🔬 **Research**: This platform is available for academic research and educational use")

# Footer
st.divider()
st.markdown(
    """
<div style='text-align: center; color: #666; font-size: 12px;'>
    © 2025 Nino Medical AI Demo | Open Source | Educational Use Only
</div>
""",
    unsafe_allow_html=True,
)
