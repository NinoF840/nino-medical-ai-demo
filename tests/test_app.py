"""Unit tests for the medical AI application."""
import pytest
import sys
import os

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMedicalAIApp:
    """Test class for medical AI application."""
    
    @pytest.mark.unit
    def test_patient_data_structure(self):
        """Test that patient data has the correct structure."""
        # Import the data from app.py
        from app import data
        
        # Check required fields are present
        assert "Patient ID" in data
        assert "Heart Rate" in data
        assert "Blood Pressure" in data
        assert "Condition" in data
        
        # Check data consistency
        assert len(data["Patient ID"]) == len(data["Heart Rate"])
        assert len(data["Patient ID"]) == len(data["Blood Pressure"])
        assert len(data["Patient ID"]) == len(data["Condition"])
    
    @pytest.mark.unit
    def test_patient_data_values(self):
        """Test that patient data values are valid."""
        from app import data
        
        # Test heart rate values are reasonable
        for hr in data["Heart Rate"]:
            assert isinstance(hr, int)
            assert 40 <= hr <= 200, f"Heart rate {hr} is out of normal range"
        
        # Test patient IDs are strings
        for pid in data["Patient ID"]:
            assert isinstance(pid, str)
            assert len(pid) > 0
        
        # Test conditions are valid
        valid_conditions = ["Stable", "Monitored", "Critical"]
        for condition in data["Condition"]:
            assert condition in valid_conditions
    
    @pytest.mark.unit
    def test_blood_pressure_format(self):
        """Test blood pressure format is correct."""
        from app import data
        
        for bp in data["Blood Pressure"]:
            assert isinstance(bp, str)
            assert "/" in bp, f"Blood pressure {bp} should contain '/'"
            
            # Split and validate systolic/diastolic
            parts = bp.split("/")
            assert len(parts) == 2
            
            systolic = int(parts[0])
            diastolic = int(parts[1])
            
            assert 80 <= systolic <= 200, f"Systolic {systolic} out of range"
            assert 40 <= diastolic <= 120, f"Diastolic {diastolic} out of range"
            assert systolic > diastolic, f"Systolic should be higher than diastolic"


class TestAIActCompliance:
    """Test AI Act compliance requirements."""
    
    @pytest.mark.unit
    def test_synthetic_data_disclaimer(self):
        """Test that synthetic data is properly disclosed."""
        # This test would verify that the app properly discloses synthetic data
        # For now, we'll just check the string exists in the app
        with open("app.py", "r") as f:
            content = f.read()
            assert "synthetic" in content.lower(), "App should disclose synthetic data"
    
    @pytest.mark.unit
    def test_medical_ai_identification(self):
        """Test that the app identifies itself as AI-powered."""
        with open("app.py", "r") as f:
            content = f.read()
            assert "AI" in content, "App should identify as AI-powered"
            assert "Medical AI" in content, "App should identify as Medical AI"
