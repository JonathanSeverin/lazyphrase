import json
from pathlib import Path
from tkinter import filedialog

from models.phrase import Phrase
from core.phrase_manipulation import validate_hotkey, validate_phrase_content, validate_phrase_title

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
      parse_phrase_list(loaded)  # Validate and parse the loaded data
      out = [Phrase(**phrase) for phrase in loaded]
      return out
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





def parse_phrase_list(phrase_data):
  if not phrase_data:
    return []


































  """ parsed_phrases = []
  for phrase in phrase_data:
    try:
      parsed_phrase = Phrase(
        title=phrase.get("title", ""),
        content=phrase.get("content", ""),
        hotkey=phrase.get("hotkey", ""),
        id=phrase.get("id", None),
        is_active=phrase.get("is_active", True)
      )
      parsed_phrases.append(parsed_phrase)
    except Exception as e:
      print(f"Error parsing phrase: {e}")

  return parsed_phrases """
  


