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


def save_to_file(data):
  with open(path, "w") as f:
    destruct = []
    for key, value in data.items():
      for phrase in value:
        destruct.append({
          "title": phrase.title,
          "content": phrase.content,
          "hotkey": phrase.hotkey,
          "is_active": phrase.is_active
        })
    json.dump(destruct, f)
  

def load_from_file():
  try:
    with open(path, "r") as f:
      loaded = json.load(f)
      dict_to_phrase = [Phrase(**phrase) for phrase in loaded]
      out_dict = {}
      for p in dict_to_phrase:
        if p.hotkey in out_dict: out_dict[p.hotkey].append(p)
        else: out_dict[p.hotkey] = [p]
      return out_dict
  except (FileNotFoundError, json.JSONDecodeError) as e: 
    print(f"Could not load phrases from file {e}")
    return {}