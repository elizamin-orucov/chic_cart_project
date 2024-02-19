import os
from core.settings import LOCAL_APPS

# Run the code to clean migrations files inside applications

# python delete_migrations.py + enter

for app in LOCAL_APPS:
    files = os.listdir(f"{app}/migrations/")
    for file in files:
        if file != "__init__.py":
            if os.path.isfile(f"{app}/migrations/{file}"):
                os.remove(f"{app}/migrations/{file}")
