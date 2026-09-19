import os

# The project is run from its repo checkout (an editable install), so config and logs
# live at the repo root, two levels above this package.
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.yaml")
LOGS_PATH = os.path.join(PROJECT_ROOT, "logs")
