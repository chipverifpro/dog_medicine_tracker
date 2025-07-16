import os
import json
import pytest
from datetime import datetime, timedelta
from dose_logger import DoseLogger

TEST_DOSE_FILE = "test_dose_log.json"

@pytest.fixture
def dose_logger():
    if os.path.exists(TEST_DOSE_FILE):
        os.remove(TEST_DOSE_FILE)
    return DoseLogger(storage_file=TEST_DOSE_FILE)

def test_log_dose(dose_logger):
    dose_logger.log_dose("HeartGuard")
    log = dose_logger.get_today_log()
    assert len(log) == 1
    assert log[0]["medication"] == "HeartGuard"

def test_prevent_double_dosing_same_day(dose_logger):
    dose_logger.log_dose("HeartGuard")
    with pytest.raises(ValueError):
        dose_logger.log_dose("HeartGuard")

def test_get_today_log(dose_logger):
    dose_logger.log_dose("NexGard")
    today_log = dose_logger.get_today_log()
    assert len(today_log) == 1
    assert today_log[0]["medication"] == "NexGard"

def test_persistence(dose_logger):
    dose_logger.log_dose("HeartGuard")
    del dose_logger
    new_instance = DoseLogger(storage_file=TEST_DOSE_FILE)
    log = new_instance.get_today_log()
    assert any(d["medication"] == "HeartGuard" for d in log)

def test_due_medications(dose_logger):
    meds = [
        {"name": "HeartGuard", "frequency": "Once daily"},
        {"name": "NexGard", "frequency": "Once monthly"}
    ]
    dose_logger.log_dose("HeartGuard")
    due = dose_logger.get_due_medications(meds)
    assert all(m["name"] != "HeartGuard" for m in due)
    assert any(m["name"] == "NexGard" for m in due)