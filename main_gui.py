import tkinter as tk
from tkinter import ttk, messagebox
from medication_manager import MedicationManager
from dose_logger import DoseLogger
import json
import smtplib
from email.message import EmailMessage
import os
import threading
import time
from datetime import datetime

SETTINGS_FILE = "settings.json"

class MedicationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dog Medicine Tracker")
        self.manager = MedicationManager()
        self.start_email_scheduler()

        self.setup_tabs()

    def setup_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.med_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.med_tab, text="Medications")
        self.setup_medication_tab()

        self.schedule_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.schedule_tab, text="Today's Schedule")
        self.setup_schedule_tab()

        self.settings_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.settings_tab, text="Settings")
        self.setup_settings_tab()

    def setup_medication_tab(self):
        frame = self.med_tab

        # Input fields
        input_frame = ttk.LabelFrame(frame, text="Add Medication")
        input_frame.pack(padx=10, pady=10, fill='x')

        ttk.Label(input_frame, text="Name").grid(row=0, column=0, sticky="e")
        self.name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.name_var, width=30).grid(row=0, column=1)

        ttk.Label(input_frame, text="Dosage").grid(row=1, column=0, sticky="e")
        self.dosage_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.dosage_var, width=30).grid(row=1, column=1)

        ttk.Label(input_frame, text="Frequency").grid(row=2, column=0, sticky="e")
        self.freq_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.freq_var, width=30).grid(row=2, column=1)

        ttk.Label(input_frame, text="Notes").grid(row=3, column=0, sticky="e")
        self.notes_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.notes_var, width=30).grid(row=3, column=1)

        ttk.Label(input_frame, text="Times per day").grid(row=4, column=0, sticky="e")
        self.times_var = tk.IntVar(value=1)
        ttk.Spinbox(input_frame, from_=1, to=10, textvariable=self.times_var, width=5).grid(row=4, column=1, sticky="w")

        ttk.Button(input_frame, text="Add Medication", command=self.add_med).grid(row=5, column=0, columnspan=2, pady=5)

        # Medication list
        list_frame = ttk.LabelFrame(frame, text="Current Medications")
        list_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.med_tree = ttk.Treeview(
            list_frame,
            columns=("Name", "Dosage", "Frequency", "Notes", "Times"),
            show="headings",
            height=8
        )

        # Define column headers
        for col in ("Name", "Dosage", "Frequency", "Notes", "Times"):
            self.med_tree.heading(col, text=col)
            self.med_tree.column(col, width=120, anchor="center")

        self.med_tree.pack(fill='both', expand=True)

        ttk.Button(list_frame, text="Remove Selected", command=self.remove_selected).pack(pady=5)

        self.refresh_med_list()


    def setup_schedule_tab(self):
        self.dose_logger = DoseLogger()

        frame = self.schedule_tab

        # Due meds section
        due_frame = ttk.LabelFrame(frame, text="Medications Due Today")
        due_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.due_tree = ttk.Treeview(due_frame, columns=("Name", "Dosage", "Frequency", "Notes", "Times"), show="headings")
        for col in ("Name", "Dosage", "Frequency", "Notes", "Times"):
            self.due_tree.heading(col, text=col)
            self.due_tree.column(col, width=120, anchor="center")
        self.due_tree.pack(fill='both', expand=True)

        ttk.Button(due_frame, text="Mark as Given", command=self.mark_selected_given).pack(pady=5)

        # Logged today section
        log_frame = ttk.LabelFrame(frame, text="Doses Already Logged Today")
        log_frame.pack(padx=10, pady=10, fill='both', expand=True)

        self.log_listbox = tk.Listbox(log_frame)
        self.log_listbox.pack(fill='both', expand=True)

        self.refresh_schedule_tab()



    def setup_settings_tab(self):
        self.settings = self.load_settings()

        frame = self.settings_tab
        form = ttk.LabelFrame(frame, text="Email Reminder Settings")
        form.pack(padx=10, pady=10, fill='x')

        # Email fields
        self.email_vars = {
            "smtp_server": tk.StringVar(value=self.settings.get("smtp_server", "smtp.gmail.com")),
            "port": tk.StringVar(value=str(self.settings.get("port", "587"))),
            "email": tk.StringVar(value=self.settings.get("email", "")),
            "password": tk.StringVar(value=self.settings.get("password", "")),
            "send_time": tk.StringVar(value=self.settings.get("send_time", "08:00"))
        }

        labels = {
            "smtp_server": "SMTP Server",
            "port": "Port",
            "email": "Email Address",
            "password": "Password",
            "send_time": "Reminder Time (HH:MM)"
        }

        for idx, (key, label) in enumerate(labels.items()):
            ttk.Label(form, text=label).grid(row=idx, column=0, sticky="e")
            entry = ttk.Entry(form, textvariable=self.email_vars[key], show="*" if "password" in key else None, width=35)
            entry.grid(row=idx, column=1, pady=2, sticky="w")

        # Buttons
        ttk.Button(form, text="Save Settings", command=self.save_settings).grid(row=5, column=0, pady=10)
        ttk.Button(form, text="Send Test Email", command=self.send_test_email).grid(row=5, column=1, pady=10)

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            with open(SETTINGS_FILE, "r") as f:
                return json.load(f)
        return {}

    def save_settings(self):
        try:
            data = {k: v.get() for k, v in self.email_vars.items()}
            with open(SETTINGS_FILE, "w") as f:
                json.dump(data, f, indent=2)
            messagebox.showinfo("Saved", "Settings saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


    def add_med(self):
        name = self.name_var.get().strip()
        dosage = self.dosage_var.get().strip()
        frequency = self.freq_var.get().strip()
        notes = self.notes_var.get().strip()
        times_per_day = self.times_var.get()

        if not name or not dosage or not frequency:
            messagebox.showerror("Missing Data", "Name, Dosage, and Frequency are required.")
            return

        try:
            self.manager.add_medication(name, dosage, frequency, notes, times_per_day)
            self.refresh_med_list()
            self.refresh_schedule_tab()
            self.name_var.set("")
            self.dosage_var.set("")
            self.freq_var.set("")
            self.notes_var.set("")
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def remove_selected(self):
        selected = self.med_tree.selection()
        if not selected:
            messagebox.showinfo("Select", "Please select a medication to remove.")
            return

        med_name = self.med_tree.item(selected[0])["values"][0]
        self.manager.remove_medication(med_name)
        self.refresh_med_list()
        self.refresh_schedule_tab()

    def refresh_med_list(self):
        for row in self.med_tree.get_children():
            self.med_tree.delete(row)

        for med in self.manager.get_all_medications():
            self.med_tree.insert("", "end", values=(
                med["name"],
                med["dosage"],
                med["frequency"],
                med["notes"],
                med.get("times_per_day", 1)
            ))

    def refresh_schedule_tab(self):
        # Refresh due meds table
        for row in self.due_tree.get_children():
            self.due_tree.delete(row)

        all_meds = self.manager.get_all_medications()
        due_meds = self.dose_logger.get_due_medications(all_meds)

        for med in due_meds:
            self.due_tree.insert("", "end", values=(
                f"{med['name']} ({med['remaining_doses']} left)",
                med["dosage"],
                med["frequency"],
                med["notes"],
                med.get("times_per_day", 1)
            ))

        # Refresh today's log list
        self.log_listbox.delete(0, tk.END)
        log = self.dose_logger.get_today_log()
        for entry in log:
            self.log_listbox.insert(tk.END, f"{entry['datetime'][:16]} — {entry['medication']}")

    def mark_selected_given(self):
        selected = self.due_tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Please select a medication to mark as given.")
            return

        name = self.due_tree.item(selected[0])["values"][0]
        try:
            self.dose_logger.log_dose(name)
            messagebox.showinfo("Success", f"Dose for '{name}' logged.")
            self.refresh_schedule_tab()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def send_test_email(self):
        try:
            self.save_settings()
            settings = self.load_settings()
            msg = EmailMessage()
            msg["Subject"] = "Test Email from Dog Medicine Tracker"
            msg["From"] = settings["email"]
            msg["To"] = settings["email"]
            msg.set_content("This is a test email to confirm that email settings are correct.")

            with smtplib.SMTP(settings["smtp_server"], int(settings["port"])) as server:
                server.starttls()
                server.login(settings["email"], settings["password"])
                server.send_message(msg)

            messagebox.showinfo("Success", "Test email sent successfully.")

        except Exception as e:
            messagebox.showerror("Email Failed", str(e))

    def start_email_scheduler(self):
        def check_and_send():
            while True:
                try:
                    settings = self.load_settings()
                    now = datetime.now().strftime("%H:%M")
                    target = settings.get("send_time", "08:00")

                    print(f"[Scheduler] Current time: {now}, Target time: {target}")

                    if now == target:
                        print("[Scheduler] Sending email...")
                        self.send_reminder_email()
                        time.sleep(60)

                except Exception as e:
                    print(f"[Scheduler] Error: {e}")

                time.sleep(30)

        def check_and_send_no_message():
            while True:
                try:
                    settings = self.load_settings()
                    now = datetime.now().strftime("%H:%M")
                    target = settings.get("send_time", "08:00")

                    if now == target:
                        self.send_reminder_email()
                        time.sleep(60)  # Avoid sending multiple times in the same minute

                except Exception as e:
                    print(f"Scheduler error: {e}")

                time.sleep(30)

        t = threading.Thread(target=check_and_send, daemon=True)
        t.start()

    def send_reminder_email(self):
        settings = self.load_settings()
        all_meds = self.manager.get_all_medications()
        due_meds = self.dose_logger.get_due_medications(all_meds)

        if not due_meds:
            return  # Nothing to send

        msg = EmailMessage()
        msg["Subject"] = "Dog Medicine Reminder"
        msg["From"] = settings["email"]
        msg["To"] = settings["email"]

        med_lines = [f"- {med['name']} ({med['dosage']}, {med['frequency']})" for med in due_meds]
        body = "The following medications are due today and have not been logged:\n\n" + "\n".join(med_lines)
        msg.set_content(body)

        try:
            with smtplib.SMTP(settings["smtp_server"], int(settings["port"])) as server:
                server.starttls()
                server.login(settings["email"], settings["password"])
                server.send_message(msg)
            print("[Reminder] Email sent.")
        except Exception as e:
            print("[Reminder] Failed to send email:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = MedicationApp(root)
    root.mainloop()