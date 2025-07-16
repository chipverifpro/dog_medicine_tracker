import json
import os

class MedicationManager:
    def __init__(self, storage_file="med_data.json"):
        self.storage_file = storage_file
        self.medications = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.storage_file):
            with open(self.storage_file, "r") as f:
                self.medications = json.load(f)
        else:
            self.medications = []

    def save_data(self):
        with open(self.storage_file, "w") as f:
            json.dump(self.medications, f, indent=2)

    def add_medication(self, name, dosage, frequency, notes="", times_per_day=1):
        # Check for duplicate
        if any(med["name"].lower() == name.lower() for med in self.medications):
            raise ValueError(f"Medication '{name}' already exists.")
        new_med = {
            "name": name, 
            "dosage": dosage,
            "frequency": frequency,
            "notes": notes,
            "times_per_day": times_per_day
        }
        self.medications.append(new_med)
        self.save_data()

    def remove_medication(self, name):
        self.medications = [med for med in self.medications if med["name"].lower() != name.lower()]
        self.save_data()

    def get_all_medications(self):
        return self.medications