import warnings
import sys
import os
import multiprocessing

# Force offline mode for all AI libraries
os.environ["TRANSFORMERS_OFFLINE"] = "1"
os.environ["HF_HUB_OFFLINE"] = "1"

# MUST be called at the very top for PyInstaller + Multiprocessing support
if __name__ == "__main__":
    multiprocessing.freeze_support()

# Silence specific library warnings for a cleaner CLI experience
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality")
warnings.filterwarnings("ignore", message="Unable to find acceptable character detection dependency")
# Silence HuggingFace weight loading warnings
warnings.filterwarnings("ignore", message=".*unauthenticated requests.*")

try:
    import requests
    from urllib3.exceptions import InsecureRequestWarning
    if hasattr(requests, 'packages'):
        requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
except Exception:
    pass

from src.cli import cli

if __name__ == "__main__":
    cli()
