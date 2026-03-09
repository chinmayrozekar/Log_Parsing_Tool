import warnings
import sys

# Silence specific library warnings for a cleaner CLI experience
warnings.filterwarnings("ignore", message="Core Pydantic V1 functionality")
# Silence Requests/Charset dependency warning
try:
    import requests
    from urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
except Exception:
    pass

from src.cli import cli

if __name__ == "__main__":
    cli()
