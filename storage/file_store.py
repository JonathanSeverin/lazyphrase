import json
from pathlib import Path
from tkinter import filedialog

from models.phrase import Phrase
from core.phrase_manipulation import validate_phrase_content, validate_phrase_title

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
          "id": phrase.id,
          "is_active": phrase.is_active
        })
      json.dump(destruct, f, indent=2, ensure_ascii=False)
  except OSError as e:
    print(f"Could not save phrases to file {e}")
  

def load_phrases(custom_path=None):
  path_to_file = path if custom_path is None else custom_path

  try:
    with open(path_to_file, "r") as f:
      loaded = json.load(f)
      if len(loaded) == 0:
        return []
      out = [Phrase(**phrase) for phrase in loaded]
      result = parse_phrase_list(out)  # Validate and parse the loaded data
      if result:
        return out
      print(f"Invalid phrase data in file {path_to_file}. Please check the file format or the content of the phrases.")
      return []
  except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Could not load phrase list from file {e}")
    return []


def locate_phrase_file():
  dialog = filedialog.askopenfilename(
    filetypes=[("JSON files", "*.json")], 
    title="Load Phrases", 
    initialdir=Path.home())
  
  if dialog:
    if isinstance(dialog, str):
      file_path = Path(dialog)
      return file_path
    else:
      return None

  return None


def parse_phrase_list(phrase_data):
  if not phrase_data:
    return False

  for p in phrase_data:
    t = validate_phrase_title(p.title)
    c = validate_phrase_content(p.content)
    # no hotkey validation yet, since that would need extraction of the actual key from the hotkey string. Implement later

    if not isinstance(p, Phrase):
      return False
    if not t or not c:
      return False

  return True