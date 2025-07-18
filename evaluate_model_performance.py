"""
Evaluate F1 Score and Model Performance for Medical AI Demo
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, f1_score
from app import generate_synthetic_data

def evaluate_model_performance(n_patients=100, random_state=42):
    """Evaluate the model performance including detailed F1 scores."""
    
    print("🏥 Medical AI Model Performance Evaluation")
    print("=" * 50)
    
    # Generate synthetic data
    df = generate_synthetic_data(n_patients)
    print(f"📊 Dataset: {len(df)} patients with {len(df.columns)-2} clinical features")
    
    # Show risk distribution
    risk_dist = df['Risk_Category'].value_counts()
    print(f"\n📈 Risk Distribution:")
    for risk, count in risk_dist.items():
        percentage = (count / len(df)) * 100
        print(f"   {risk}: {count} patients ({percentage:.1f}%)")
    
    # Prepare features for ML
    numeric_cols = ['Age', 'Heart_Rate', 'Systolic_BP', 'Diastolic_BP', 'Temperature', 'Blood_Sugar']
    X = df[numeric_cols]
    y = df['Risk_Category']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=random_state)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Train Random Forest model
    rf_model = RandomForestClassifier(n_estimators=100, random_state=random_state)
    rf_model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = rf_model.predict(X_test_scaled)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    
    # Calculate F1 scores
    f1_macro = f1_score(y_test, y_pred, average='macro')
    f1_weighted = f1_score(y_test, y_pred, average='weighted')
    f1_micro = f1_score(y_test, y_pred, average='micro')
    
    # Get per-class F1 scores
    f1_per_class = f1_score(y_test, y_pred, average=None)
    unique_classes = sorted(y.unique())
    
    print(f"\n🤖 Model Performance Results:")
    print(f"   Overall Accuracy: {accuracy:.3f} ({accuracy:.1%})")
    print(f"\n🎯 F1 Score Analysis:")
    print(f"   • Macro F1 Score:    {f1_macro:.3f} ({f1_macro:.1%})")
    print(f"   • Weighted F1 Score: {f1_weighted:.3f} ({f1_weighted:.1%})")
    print(f"   • Micro F1 Score:    {f1_micro:.3f} ({f1_micro:.1%})")
    
    print(f"\n📊 Per-Class F1 Scores:")
    for i, class_name in enumerate(unique_classes):
        print(f"   • {class_name}: {f1_per_class[i]:.3f} ({f1_per_class[i]:.1%})")
    
    # Interpretation
    print(f"\n📋 F1 Score Interpretation:")
    if f1_macro >= 0.80:
        print("   ✅ EXCELLENT: F1 score > 0.80 indicates excellent performance")
    elif f1_macro >= 0.70:
        print("   ✅ GOOD: F1 score 0.70-0.80 indicates good performance")
    elif f1_macro >= 0.60:
        print("   ⚠️  FAIR: F1 score 0.60-0.70 indicates fair performance")
    elif f1_macro >= 0.50:
        print("   ⚠️  POOR: F1 score 0.50-0.60 indicates poor performance")
    else:
        print("   ❌ VERY POOR: F1 score < 0.50 indicates very poor performance")
    
    # Additional insights
    print(f"\n💡 Additional Insights:")
    print(f"   • Test set size: {len(y_test)} patients")
    print(f"   • Training set size: {len(y_train)} patients")
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'Feature': numeric_cols,
        'Importance': rf_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print(f"\n🔍 Most Important Features:")
    for i, row in feature_importance.head(3).iterrows():
        print(f"   {i+1}. {row['Feature']}: {row['Importance']:.3f}")
    
    # Show full classification report
    print(f"\n📄 Detailed Classification Report:")
    print(classification_report(y_test, y_pred))
    
    return {
        'accuracy': accuracy,
        'f1_macro': f1_macro,
        'f1_weighted': f1_weighted,
        'f1_micro': f1_micro,
        'f1_per_class': dict(zip(unique_classes, f1_per_class)),
        'feature_importance': feature_importance
    }

if __name__ == "__main__":
    results = evaluate_model_performance()
