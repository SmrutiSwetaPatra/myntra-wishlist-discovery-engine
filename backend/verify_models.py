import os
from google import genai
from dotenv import load_dotenv

def main():
    load_dotenv()
    client = genai.Client()
    
    print("Available Embedding Models:")
    # We want to filter for models that support EMBED_CONTENT
    models = client.models.list()
    for m in models:
        # Check if it supports embedding
        if "EMBED_CONTENT" in [a for a in getattr(m, 'supported_actions', [])]:
            print(f"- {m.name}")
        # Or just print all models with "embed" in the name
        elif "embed" in m.name.lower():
            print(f"- {m.name} (by name)")

if __name__ == "__main__":
    main()
