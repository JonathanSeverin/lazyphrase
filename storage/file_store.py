import json

from models import Phrase

GLOBAL_PATH_TO_PHRASES = "~/.local/share/phraseexpander/phrases.json"


def save_to_file(data):
  try:
    with open(GLOBAL_PATH_TO_PHRASES, "w") as f:
      destruct = []
      for key, value in data.items():
        phr_to_dict = {}
        phr_to_dict.update(key, value)
        destruct.append(phr_to_dict)

      json.dump(destruct, f)
  except (FileNotFoundError) as e:
    print(f"failed to save phrases {e}")


def load_from_file():
  try:
    with open(GLOBAL_PATH_TO_PHRASES, "r") as f:
      loaded = json.load(f)
      dict_to_phrase = [Phrase(**phrase) for phrase in loaded]
      out_dict = {}
      for p in dict_to_phrase:
        if p.hotkey in out_dict: out_dict[p.hotkey].append(p)
        else: out_dict.update(p.hotkey, [p])
      return out_dict
  except (FileNotFoundError) as e: 
    print(f"Could not load phrases from file {e}")