## Dog Medicine Tracker

This is a simple little app that you can put a list of medications into, and then
mark when one is taken.  It has a nice GUI, stores all it's data between runs,
and can even send reminder emails.

This is a 100% vibe-coded app.  I used ChatGPT4o and Visual Studio Code on a Mac.
It took about 4 hours.  I did not make any changes that ChatGPT didn't tell me to
make.  It included some debugging sessions where things weren't installed right
(or at all).  It made a few mistakes, and upon pointing them out, it was able to
correct them.

Here's a couple exerpts from the log showing the initial instructions, and the plan.

> I want you to help write a program in Python called Dog Medicine Tracker.
> We will walk through the process step by step.  First, we will define the
> goals and specifications for the program.  Then we will outline the
> structure of the program.  Next, we will use Test Driven Methodology to
> write tests and functions for each piece.  I will copy the code into an
> IDE and let you know if there are any errors that need to be addressed.

```
✅ Final Goals and Specifications for Dog Medicine Tracker

Core Features
	1.	Medication Records
	•	Medication name
	•	Dosage
	•	Frequency (e.g., once a day, twice a day)
	•	Notes (e.g., with food, side effects)
	2.	Daily Schedule
	•	Show which meds need to be given today
	•	Highlight missed or upcoming doses
	3.	Logging Administered Doses
	•	Record timestamp when a dose is given
	•	Prevent accidental double-dosing
	4.	Data Persistence
	•	Store medication records and dose logs in a local file (e.g., JSON or SQLite)
	5.	Simple GUI
	•	Add/edit medications
	•	View today’s meds
	•	Mark doses as given
	•	View logs
	6.	Email Reminders
	•	Optional email alerts for scheduled meds
	•	Configurable email address and time of day

⸻

✅ Next Step: Outline the Program Structure

Let’s map out the components/modules:

Data Layer
	•	med_data.json or med_data.db
	•	Handles loading/saving medication records and logs

Core Logic (Python Classes/Functions)
	•	MedicationManager: CRUD for medications
	•	DoseLogger: Log doses, check what’s due
	•	ReminderScheduler: Schedule and send email reminders

GUI (Tkinter-based)
	•	Medication entry form
	•	Today’s schedule view
	•	Dose log viewer
	•	Settings (email config)

Email Module
	•	SMTP-based
	•	Pulls today’s schedule and sends reminders
 ```
