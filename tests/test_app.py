"""Unit tests for the medical AI application."""

import os
import sys

import pytest

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMedicalAIApp:
    """Test class for medical AI application."""

    @pytest.mark.unit
    def test_synthetic_data_generation_functionality(self):
        """Test that synthetic data generation works correctly."""
        from app import generate_synthetic_data
        
        # Generate test data
        test_df = generate_synthetic_data(20)
        
        # Check basic structure
        assert len(test_df) == 20, "Should generate specified number of patients"
        
        # Check required columns exist
        expected_cols = ['Patient_ID', 'Age', 'Heart_Rate', 'Systolic_BP', 
                        'Diastolic_BP', 'Temperature', 'Blood_Sugar', 
                        'Risk_Category', 'Risk_Score']
        
        for col in expected_cols:
            assert col in test_df.columns, f"Column {col} should be present"

    @pytest.mark.unit
    def test_patient_data_values(self):
        """Test that patient data values are valid."""
        from app import generate_synthetic_data
        
        test_df = generate_synthetic_data(10)

        # Test heart rate values are reasonable
        for hr in test_df['Heart_Rate']:
            assert isinstance(hr, (int, int)) 
            assert 30 <= hr <= 180, f"Heart rate {hr} is out of reasonable range"

        # Test patient IDs are strings
        for pid in test_df['Patient_ID']:
            assert isinstance(pid, str)
            assert len(pid) > 0

        # Test risk categories are valid
        valid_conditions = ["Low Risk", "Medium Risk", "High Risk"]
        for condition in test_df['Risk_Category']:
            assert condition in valid_conditions

    @pytest.mark.unit
    def test_blood_pressure_values(self):
        """Test blood pressure values are correct."""
        from app import generate_synthetic_data
        
        test_df = generate_synthetic_data(10)

        # Test systolic and diastolic values
        for i, row in test_df.iterrows():
            systolic = row['Systolic_BP']
            diastolic = row['Diastolic_BP']
            
            assert isinstance(systolic, (int, int))
            assert isinstance(diastolic, (int, int))
            
            assert 80 <= systolic <= 200, f"Systolic {systolic} out of range"
            assert 40 <= diastolic <= 120, f"Diastolic {diastolic} out of range"
            assert systolic > diastolic, f"Systolic {systolic} should be higher than diastolic {diastolic}"


class TestAIActCompliance:
    """Test AI Act compliance requirements."""

    @pytest.mark.unit
    def test_synthetic_data_disclaimer(self):
        """Test that synthetic data is properly disclosed."""
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
            assert "synthetic" in content.lower(), "App should disclose synthetic data"

    @pytest.mark.unit
    def test_medical_ai_identification(self):
        """Test that the app identifies itself as AI-powered."""
        with open("app.py", "r", encoding="utf-8") as f:
            content = f.read()
            assert "AI" in content, "App should identify as AI-powered"
            assert "Medical AI" in content, "App should identify as Medical AI"


class TestMachineLearningComponents:
    """Test machine learning functionality."""

    @pytest.mark.unit
    def test_sklearn_imports(self):
        """Test that scikit-learn components can be imported."""
        try:
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.cluster import KMeans
            from sklearn.preprocessing import StandardScaler
            from sklearn.model_selection import train_test_split
            from sklearn.metrics import accuracy_score
        except ImportError as e:
            pytest.fail(f"Failed to import scikit-learn components: {e}")

    @pytest.mark.unit
    def test_synthetic_data_generation(self):
        """Test synthetic data generation function."""
        from app import generate_synthetic_data
        
        df = generate_synthetic_data(50)
        
        # Check data structure
        assert len(df) == 50, "Should generate specified number of patients"
        expected_cols = ['Patient_ID', 'Age', 'Heart_Rate', 'Systolic_BP', 
                        'Diastolic_BP', 'Temperature', 'Blood_Sugar', 
                        'Risk_Category', 'Risk_Score']
        
        for col in expected_cols:
            assert col in df.columns, f"Column {col} should be present"
        
        # Check data types and ranges
        assert df['Age'].min() >= 18, "Age should be >= 18"
        assert df['Age'].max() <= 85, "Age should be <= 85"
        assert df['Heart_Rate'].min() > 0, "Heart rate should be positive"
        assert df['Temperature'].min() > 90, "Temperature should be reasonable"
        
        # Check risk categories
        valid_risks = ['Low Risk', 'Medium Risk', 'High Risk']
        assert all(risk in valid_risks for risk in df['Risk_Category']), \
            "All risk categories should be valid"

    @pytest.mark.unit
    def test_ml_model_functionality(self):
        """Test that ML models can be trained and used."""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.preprocessing import StandardScaler
        import numpy as np
        import pandas as pd
        
        # Create minimal test data
        np.random.seed(42)
        test_data = {
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.normal(0, 1, 100),
            'target': np.random.choice(['A', 'B', 'C'], 100)
        }
        df = pd.DataFrame(test_data)
        
        # Test model training
        X = df[['feature1', 'feature2']]
        y = df['target']
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X_train_scaled, y_train)
        
        # Test predictions
        predictions = model.predict(X_test_scaled)
        assert len(predictions) == len(y_test), "Should predict for all test samples"
        assert all(pred in ['A', 'B', 'C'] for pred in predictions), \
            "All predictions should be valid classes"
