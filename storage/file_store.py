import json
from pathlib import Path

from models.phrase import Phrase

path = (
  Path.home() 
  / ".local" 
  / "share" 
  / "phraseexpander" 
  / "phrases.json"
)

path.parent.mkdir(parents=True, exist_ok=True)  # Ensure the directory exists


def save_phrases(data):
  try:
    with open(path, "w") as f:
      destruct = []
      for phrase in data:
        destruct.append({
          "title": phrase.title,
          "content": phrase.content,
          "hotkey": phrase.hotkey,
          "is_active": phrase.is_active
        })
      json.dump(destruct, f, indent=2, ensure_ascii=False)
  except OSError as e:
    print(f"Could not save phrases to file {e}")
  

def load_phrases():
  try:
    with open(path, "r") as f:
      loaded = json.load(f)
      out = [Phrase(**phrase) for phrase in loaded]
      return out
  except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Could not load phrase list from file {e}")
    return []