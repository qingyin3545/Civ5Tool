import os

USER_HOME = os.environ.get("USERPROFILE", "")

CIV5_DIR = os.path.join(
    USER_HOME, "Documents", "My Games", "Sid Meier's Civilization 5"
)