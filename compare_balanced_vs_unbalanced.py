"""
Compare Balanced vs Unbalanced Dataset Performance for Medical AI
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, f1_score, confusion_matrix
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
import warnings
warnings.filterwarnings('ignore')

def generate_unbalanced_data(n_patients=500, random_state=42):
    """Generate realistic unbalanced medical data (like real world)."""
    np.random.seed(random_state)
    
    data = {
        "Patient_ID": [f"P{i:03d}" for i in range(1, n_patients + 1)],
        "Age": np.random.randint(18, 85, n_patients),
        "Heart_Rate": np.random.normal(75, 12, n_patients).astype(int),
        "Systolic_BP": np.random.normal(120, 15, n_patients).astype(int),
        "Diastolic_BP": np.random.normal(80, 10, n_patients).astype(int),
        "Temperature": np.random.normal(98.6, 1.2, n_patients).round(1),
        "Blood_Sugar": np.random.normal(100, 20, n_patients).astype(int),
    }
    
    # Create realistic risk distribution (unbalanced - like real world)
    risk_scores = []
    for i in range(n_patients):
        score = 0
        if data["Age"][i] > 65: score += 2
        if data["Heart_Rate"][i] > 100 or data["Heart_Rate"][i] < 60: score += 1
        if data["Systolic_BP"][i] > 140: score += 2
        if data["Diastolic_BP"][i] > 90: score += 1
        if data["Blood_Sugar"][i] > 126: score += 1
        risk_scores.append(score)
    
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

def generate_balanced_data(n_patients=500, random_state=42):
    """Generate artificially balanced data for comparison."""
    np.random.seed(random_state)
    patients_per_class = n_patients // 3
    
    all_data = []
    
    # Generate Low Risk patients
    for i in range(patients_per_class):
        patient = {
            "Patient_ID": f"L{i:03d}",
            "Age": np.random.randint(18, 50),  # Younger
            "Heart_Rate": np.random.randint(60, 90),  # Normal
            "Systolic_BP": np.random.randint(90, 120),  # Normal
            "Diastolic_BP": np.random.randint(60, 80),  # Normal
            "Temperature": np.random.normal(98.6, 0.5),  # Normal
            "Blood_Sugar": np.random.randint(80, 110),  # Normal
            "Risk_Category": "Low Risk",
            "Risk_Score": 0
        }
        all_data.append(patient)
    
    # Generate Medium Risk patients
    for i in range(patients_per_class):
        patient = {
            "Patient_ID": f"M{i:03d}",
            "Age": np.random.randint(45, 70),  # Middle-aged
            "Heart_Rate": np.random.randint(55, 105),  # Slightly abnormal
            "Systolic_BP": np.random.randint(115, 145),  # Slightly high
            "Diastolic_BP": np.random.randint(75, 95),  # Slightly high
            "Temperature": np.random.normal(98.8, 0.8),  # Slightly elevated
            "Blood_Sugar": np.random.randint(95, 130),  # Slightly high
            "Risk_Category": "Medium Risk",
            "Risk_Score": 2
        }
        all_data.append(patient)
    
    # Generate High Risk patients
    for i in range(patients_per_class):
        patient = {
            "Patient_ID": f"H{i:03d}",
            "Age": np.random.randint(65, 85),  # Older
            "Heart_Rate": np.random.choice([45, 50, 55, 110, 120, 130]),  # Abnormal
            "Systolic_BP": np.random.randint(140, 180),  # High
            "Diastolic_BP": np.random.randint(90, 120),  # High
            "Temperature": np.random.normal(99.2, 1.0),  # Elevated
            "Blood_Sugar": np.random.randint(125, 200),  # High
            "Risk_Category": "High Risk",
            "Risk_Score": 5
        }
        all_data.append(patient)
    
    # Add remaining patients to balance exactly
    remaining = n_patients - len(all_data)
    for i in range(remaining):
        patient = all_data[i % len(all_data)].copy()
        patient["Patient_ID"] = f"X{i:03d}"
        all_data.append(patient)
    
    return pd.DataFrame(all_data)

def evaluate_dataset(df, dataset_name, use_class_weights=False):
    """Evaluate a dataset and return performance metrics."""
    print(f"\n{'='*60}")
    print(f"📊 {dataset_name}")
    print(f"{'='*60}")
    
    # Show distribution
    risk_dist = df['Risk_Category'].value_counts()
    print(f"📈 Class Distribution:")
    total = len(df)
    for risk, count in risk_dist.items():
        percentage = (count / total) * 100
        print(f"   {risk}: {count:3d} patients ({percentage:5.1f}%)")
    
    # Calculate balance ratio
    max_class = risk_dist.max()
    min_class = risk_dist.min()
    balance_ratio = min_class / max_class
    print(f"⚖️  Balance Ratio: {balance_ratio:.3f} (1.0 = perfectly balanced)")
    
    # Prepare features
    numeric_cols = ['Age', 'Heart_Rate', 'Systolic_BP', 'Diastolic_BP', 'Temperature', 'Blood_Sugar']
    X = df[numeric_cols]
    y = df['Risk_Category']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # Set up class weights if requested
    class_weight = None
    if use_class_weights:
        classes = np.unique(y_train)
        weights = compute_class_weight('balanced', classes=classes, y=y_train)
        class_weight = dict(zip(classes, weights))
        print(f"🏋️  Using Class Weights: {class_weight}")
    
    # Train model
    rf_model = RandomForestClassifier(
        n_estimators=100, 
        random_state=42,
        class_weight=class_weight
    )
    rf_model.fit(X_train_scaled, y_train)
    
    # Make predictions
    y_pred = rf_model.predict(X_test_scaled)
    
    # Calculate metrics
    accuracy = accuracy_score(y_test, y_pred)
    f1_macro = f1_score(y_test, y_pred, average='macro')
    f1_weighted = f1_score(y_test, y_pred, average='weighted')
    f1_micro = f1_score(y_test, y_pred, average='micro')
    
    # Per-class F1 scores
    f1_per_class = f1_score(y_test, y_pred, average=None)
    unique_classes = sorted(y.unique())
    
    print(f"\n🤖 Performance Metrics:")
    print(f"   Overall Accuracy:    {accuracy:.3f} ({accuracy:.1%})")
    print(f"   Macro F1 Score:      {f1_macro:.3f} ({f1_macro:.1%})")
    print(f"   Weighted F1 Score:   {f1_weighted:.3f} ({f1_weighted:.1%})")
    print(f"   Micro F1 Score:      {f1_micro:.3f} ({f1_micro:.1%})")
    
    print(f"\n📊 Per-Class F1 Scores:")
    class_f1_dict = {}
    for i, class_name in enumerate(unique_classes):
        class_f1_dict[class_name] = f1_per_class[i]
        print(f"   • {class_name:12s}: {f1_per_class[i]:.3f} ({f1_per_class[i]:.1%})")
    
    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred, labels=unique_classes)
    print(f"\n🔍 Confusion Matrix:")
    print(f"   Predicted:  {' '.join([f'{cls:>8s}' for cls in unique_classes])}")
    for i, true_class in enumerate(unique_classes):
        row = ' '.join([f'{cm[i][j]:8d}' for j in range(len(unique_classes))])
        print(f"   {true_class:9s}: {row}")
    
    return {
        'accuracy': accuracy,
        'f1_macro': f1_macro,
        'f1_weighted': f1_weighted,
        'f1_micro': f1_micro,
        'f1_per_class': class_f1_dict,
        'balance_ratio': balance_ratio,
        'class_distribution': risk_dist.to_dict()
    }

def main():
    print("🏥 BALANCED vs UNBALANCED DATASET COMPARISON")
    print("=" * 80)
    
    # Generate datasets
    unbalanced_df = generate_unbalanced_data(500, random_state=42)
    balanced_df = generate_balanced_data(500, random_state=42)
    
    # Evaluate datasets
    unbalanced_results = evaluate_dataset(unbalanced_df, "UNBALANCED DATASET (Realistic)", use_class_weights=False)
    unbalanced_weighted_results = evaluate_dataset(unbalanced_df, "UNBALANCED DATASET (With Class Weights)", use_class_weights=True)
    balanced_results = evaluate_dataset(balanced_df, "BALANCED DATASET (Artificial)", use_class_weights=False)
    
    # Summary comparison
    print(f"\n{'='*80}")
    print(f"📋 SUMMARY COMPARISON")
    print(f"{'='*80}")
    
    datasets = [
        ("Unbalanced (No Weights)", unbalanced_results),
        ("Unbalanced (With Weights)", unbalanced_weighted_results),
        ("Balanced (Artificial)", balanced_results)
    ]
    
    print(f"{'Dataset':<25} {'Accuracy':<10} {'Macro F1':<10} {'High Risk F1':<12} {'Balance':<10}")
    print(f"{'-'*75}")
    
    for name, results in datasets:
        high_risk_f1 = results['f1_per_class'].get('High Risk', 0.0)
        print(f"{name:<25} {results['accuracy']:<10.3f} {results['f1_macro']:<10.3f} "
              f"{high_risk_f1:<12.3f} {results['balance_ratio']:<10.3f}")
    
    print(f"\n💡 RECOMMENDATIONS:")
    print(f"{'='*80}")
    
    # Determine best approach
    best_macro_f1 = max(results['f1_macro'] for _, results in datasets)
    best_high_risk = max(results['f1_per_class'].get('High Risk', 0.0) for _, results in datasets)
    
    print(f"🎯 FOR MEDICAL AI APPLICATIONS:")
    print(f"   • If you prioritize detecting ALL risk levels equally:")
    print(f"     → Use BALANCED data or UNBALANCED with class weights")
    print(f"     → Best Macro F1: {best_macro_f1:.3f}")
    print(f"")
    print(f"   • If you prioritize HIGH RISK detection (medical safety):")
    print(f"     → Use UNBALANCED with class weights or BALANCED data")
    print(f"     → Best High Risk F1: {best_high_risk:.3f}")
    print(f"")
    print(f"   • If you want realistic performance (like real world):")
    print(f"     → Use UNBALANCED data (shows true clinical performance)")
    print(f"     → Balance Ratio: {unbalanced_results['balance_ratio']:.3f}")
    print(f"")
    print(f"🏆 RECOMMENDATION FOR YOUR DEMO:")
    if best_macro_f1 > 0.8 and best_high_risk > 0.7:
        print(f"     ✅ Use UNBALANCED data with CLASS WEIGHTS")
        print(f"        - Realistic distribution + Better minority class detection")
        print(f"        - Best of both worlds for medical AI")
    else:
        print(f"     ✅ Use BALANCED data for educational purposes")
        print(f"        - Shows clearer model capabilities")
        print(f"        - Better for learning and demonstration")

if __name__ == "__main__":
    main()
