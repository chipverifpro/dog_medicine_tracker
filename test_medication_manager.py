import os
import json
import pytest
from medication_manager import MedicationManager

TEST_FILE = "test_med_data.json"

@pytest.fixture
def med_manager():
    # Clean test environment
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    return MedicationManager(storage_file=TEST_FILE)

def test_add_medication(med_manager):
    med_manager.add_medication("HeartGuard", "10mg", "Once daily", "Give with food")
    meds = med_manager.get_all_medications()
    assert len(meds) == 1
    assert meds[0]["name"] == "HeartGuard"

def test_prevent_duplicate_medication(med_manager):
    med_manager.add_medication("HeartGuard", "10mg", "Once daily", "Give with food")
    with pytest.raises(ValueError):
        med_manager.add_medication("HeartGuard", "10mg", "Once daily", "Give with food")

def test_remove_medication(med_manager):
    med_manager.add_medication("NexGard", "5mg", "Once monthly", "")
    med_manager.remove_medication("NexGard")
    meds = med_manager.get_all_medications()
    assert meds == []

def test_get_all_medications(med_manager):
    med_manager.add_medication("HeartGuard", "10mg", "Once daily", "Give with food")
    med_manager.add_medication("NexGard", "5mg", "Once monthly", "")
    meds = med_manager.get_all_medications()
    assert len(meds) == 2

def test_persistence(med_manager):
    med_manager.add_medication("HeartGuard", "10mg", "Once daily", "Give with food")
    del med_manager  # Simulate program close
    new_instance = MedicationManager(storage_file=TEST_FILE)
    meds = new_instance.get_all_medications()
    assert meds[0]["name"] == "HeartGuard"