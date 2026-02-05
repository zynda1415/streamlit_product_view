"""
COMMON ERRORS & FIXES – Streamlit + Google Sheets
"""

ERRORS = {
    "SpreadsheetNotFound": {
        "cause": "Sheet name is wrong OR not shared with service account",
        "fix": "Share sheet with client_email & recheck name"
    },

    "Invalid JWT Signature": {
        "cause": "private_key formatting issue",
        "fix": "Ensure \\n exists inside private_key"
    },

    "ModuleNotFoundError": {
        "cause": "requirements.txt missing library",
        "fix": "Add missing library and redeploy"
    },

    "403 PERMISSION_DENIED": {
        "cause": "Drive API or Sheets API not enabled",
        "fix": "Enable both APIs in Google Cloud"
    }
}

def show_errors():
    for k, v in ERRORS.items():
        print(f"\n{k}")
        print("Cause:", v["cause"])
        print("Fix:", v["fix"])


if __name__ == "__main__":
    show_errors()
