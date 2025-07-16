import json
import os
from datetime import datetime, date

class DoseLogger:
    def __init__(self, storage_file="dose_log.json"):
        self.storage_file = storage_file
        self.dose_log = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                self.dose_log = json.load(f)
        else:
            self.dose_log = []

    def save_data(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.dose_log, f, indent=2)

    def log_dose(self, medication_name):
        today_str = date.today().isoformat()
        meds_today = [entry for entry in self.dose_log
                    if entry["medication"].lower() == medication_name.lower()
                    and entry["date"] == today_str]

        # Load med info to get max doses
        all_meds = MedicationManager().get_all_medications()
        med_info = next((m for m in all_meds if m["name"].lower() == medication_name.lower()), None)

        if med_info is None:
            raise ValueError(f"Medication '{medication_name}' not found.")

        allowed_doses = int(med_info.get("times_per_day", 1))
        if len(meds_today) >= allowed_doses:
            raise ValueError(f"All {allowed_doses} doses of '{medication_name}' already logged today.")

        # Log the dose
        new_entry = {
            "medication": medication_name,
            "datetime": datetime.now().isoformat(),
            "date": today_str
        }
        self.dose_log.append(new_entry)
        self.save_data()
        
    def log_dose_old(self, medication_name):
        today_str = date.today().isoformat()
        # Prevent double-dosing on same day
        for entry in self.dose_log:
            if entry["medication"].lower() == medication_name.lower() and entry["date"] == today_str:
                raise ValueError(f"Dose for '{medication_name}' already logged today.")

        new_entry = {
            "medication": medication_name,
            "datetime": datetime.now().isoformat(),
            "date": today_str
        }
        self.dose_log.append(new_entry)
        self.save_data()

    def get_today_log(self):
        today_str = date.today().isoformat()
        return [entry for entry in self.dose_log if entry["date"] == today_str]

    def get_due_medications(self, med_list):
        today_given = {}
        for entry in self.get_today_log():
            name = entry["medication"].lower()
            today_given[name] = today_given.get(name, 0) + 1

        due = []
        for med in med_list:
            name = med["name"].lower()
            total_required = int(med.get("times_per_day", 1))
            given = today_given.get(name, 0)
            if given < total_required:
                remaining = total_required - given
                med_copy = med.copy()
                med_copy["remaining_doses"] = remaining
                due.append(med_copy)

        return due

    def get_due_medications_old(self, med_list):
        """Returns a list of medications from med_list that have NOT been given today."""
        today_given = {entry["medication"].lower() for entry in self.get_today_log()}
        due = [med for med in med_list if med["name"].lower() not in today_given]
        return due