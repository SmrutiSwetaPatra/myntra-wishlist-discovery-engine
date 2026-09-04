import os
import sys

# Add backend to path so we can import app
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.core.config import settings

def safe_fingerprint(key):
    if not key:
        return "None"
    if len(key) <= 8:
        return "***"
    return f"{key[:4]}...{key[-4:]}"

print("="*50)
print("GEMINI API KEY DIAGNOSTIC")
print("="*50)

# 1. From settings (Pydantic BaseSettings)
print(f"1. Key loaded by app.core.config.settings: {safe_fingerprint(settings.GEMINI_API_KEY)}")

# 2. Raw os.environ
print(f"2. Key from raw os.environ: {safe_fingerprint(os.environ.get('GEMINI_API_KEY'))}")

# 3. Read directly from backend/.env file
env_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
env_file_key = None
if os.path.exists(env_file_path):
    with open(env_file_path, "r") as f:
        for line in f:
            if line.startswith("GEMINI_API_KEY="):
                env_file_key = line.split("=", 1)[1].strip().strip('"').strip("'")
                break
print(f"3. Key physically inside backend/.env: {safe_fingerprint(env_file_key)}")

# 4. Read directly from Streamlit secrets (if exists)
streamlit_secrets_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".streamlit", "secrets.toml")
st_secrets_key = None
if os.path.exists(streamlit_secrets_path):
    import toml
    try:
        secrets = toml.load(streamlit_secrets_path)
        st_secrets_key = secrets.get("GEMINI_API_KEY")
    except Exception as e:
        st_secrets_key = f"Error reading secrets: {e}"
print(f"4. Key in .streamlit/secrets.toml: {safe_fingerprint(st_secrets_key)}")
