"""
Integration and unit tests for Automobile Service Diagnosis Assistant.
"""

import requests
import sys

BASE_URL = "http://127.0.0.1:8000"


def run_tests():
    print("==================================================")
    print(" AUTOMOBILE SERVICE DIAGNOSIS ASSISTANT TEST SUITE ")
    print("==================================================")

    # 1. Test Health Endpoint
    print("\n[1] Testing GET /api/health...")
    h = requests.get(f"{BASE_URL}/api/health")
    assert h.status_code == 200, f"Health check failed: {h.text}"
    assert h.json() == {"status": "running"}, "Health payload mismatch"
    print("  --> PASS: Health check status is running.")

    # 2. Test 10 Common Problems & Unrecognized Symptom Fallback
    print("\n[2] Testing POST /api/diagnose on 10 Automobile Issues + Fallback...")
    test_cases = [
        ("Car", "Car wont start clicking noise", "Battery & Starting System Problem", "Medium"),
        ("SUV", "Engine is overheating and boiling coolant", "Engine Overheating", "Urgent"),
        ("Bike", "Brake squeal and soft pedal", "Brake System Malfunction", "High"),
        ("Car", "Punctured flat tire on the highway", "Tyre Puncture or Pressure Loss", "High"),
        ("Van", "Low engine oil pressure warning light", "Engine Oil & Lubrication Issue", "High"),
        ("Car", "AC not cooling blowing warm air", "Air Conditioning (AC) Not Cooling", "Low"),
        ("Bike", "Engine misfire and rough idle jerking", "Engine Cylinder Misfire", "Medium"),
        ("SUV", "Sluggish poor acceleration struggling uphill", "Poor Acceleration & Power Loss", "Medium"),
        ("Car", "Check engine light came on dashboard", "Check Engine Light (MIL) Illuminated", "Medium"),
        ("Van", "Alternator battery light and dim lights", "Alternator & Charging System Failure", "High"),
        ("Car", "Mysterious vibrating cup holder sound", "Unrecognized Vehicle Issue", "Medium"),
    ]

    for vehicle, symptom, expected_problem, expected_severity in test_cases:
        res = requests.post(f"{BASE_URL}/api/diagnose", json={"vehicle": vehicle, "symptom": symptom})
        assert res.status_code == 200, f"Diagnose failed for {symptom}: {res.text}"
        data = res.json()
        assert data["problem"] == expected_problem, f"Expected {expected_problem}, got {data['problem']}"
        assert data["severity"] == expected_severity, f"Expected {expected_severity}, got {data['severity']}"
        assert len(data["basic_checks"]) > 0, "Basic checks list is empty"
        assert len(data["recommended_action"]) > 0, "Recommended action is empty"
        assert "disclaimer" in data, "Missing disclaimer field"
        print(f"  --> PASS: [{vehicle}] '{symptom[:30]}...' -> {expected_problem} (Severity: {expected_severity})")

    # 3. Test Empty Symptom Validation Handling
    print("\n[3] Testing empty input validation handling...")
    bad_res = requests.post(f"{BASE_URL}/api/diagnose", json={"vehicle": "Car", "symptom": "   "})
    assert bad_res.status_code == 400, "Empty symptom should return HTTP 400"
    print("  --> PASS: HTTP 400 returned correctly for empty input.")

    # 4. Test History Retrieval
    print("\n[4] Testing GET /api/history...")
    hist_res = requests.get(f"{BASE_URL}/api/history")
    assert hist_res.status_code == 200, "History fetch failed"
    records = hist_res.json()
    assert len(records) >= len(test_cases), "Expected history records to be saved in SQLite database"
    print(f"  --> PASS: Successfully retrieved {len(records)} history records from SQLite.")

    print("\n==================================================")
    print("  ALL TESTS PASSED SUCCESSFULLY! (100% WORKING)   ")
    print("==================================================")


if __name__ == "__main__":
    run_tests()
