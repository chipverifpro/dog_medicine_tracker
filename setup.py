from setuptools import setup

APP = ['main_gui.py']
DATA_FILES = ['med_data.json', 'dose_log.json', 'settings.json']
OPTIONS = {
    'argv_emulation': True,
    'packages': ['tkinter', 'smtplib', 'email'],
    'includes': ['medication_manager', 'dose_logger'],
    'iconfile': 'dog.icns',  # optional custom icon
    'plist': {
        'CFBundleName': 'Dog Medicine Tracker',
        'CFBundleDisplayName': 'Dog Medicine Tracker',
        'CFBundleGetInfoString': "Track your dog's meds with style",
        'CFBundleIdentifier': 'com.markpontius.dogmeds',
        'CFBundleVersion': '1.0.0',
        'CFBundleShortVersionString': '1.0.0',
    },
}

setup(
    app=APP,
    name='Dog Medicine Tracker',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)