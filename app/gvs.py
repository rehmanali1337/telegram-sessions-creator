import os

INPUT_DIR = "Input"
OUTPUT_DIR = "Output"
TELETHON_SESSIONS_DIR = f"{OUTPUT_DIR}/TelethonSessions"
PYROGRAM_SESSIONS_DIR = f"{OUTPUT_DIR}/PyrogramSessions"

STARTUP_DIRS = [INPUT_DIR, OUTPUT_DIR, TELETHON_SESSIONS_DIR, PYROGRAM_SESSIONS_DIR]


for d in STARTUP_DIRS:
    os.makedirs(d, exist_ok=True)

# Input Files

STARTUP_FILES: list[str] = []

for f in STARTUP_FILES:
    if not os.path.exists(f):
        with open(f, "w", encoding="UTF-8") as _:
            pass
