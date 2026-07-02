from core.hotkeys import start_listener
from core.expander import insert_text
from models.phrase import Phrase
from storage.file_store import save_to_file, load_from_file

from features.popup import show_popup

phrase1 = Phrase(
  "IKEA sim i post", 
  "Følgende skjer nå for deg:" \
  "Du mottar i post til folkeregistrert adresse i løpet av 2-5 virkedager",
  "alt+t",
  True
)

phrase2 = Phrase(
  "IKEA hentesim", 
  "Følgende skjer nå for deg:" \
  "Du henter sim på hvilken som helst Narvesen/7-eleven",
  "alt+t",
  True
)

phrase3 = Phrase(
  "Hei Jonathan", 
  "Hei, du snakker med Jonathan!"
  "a+shift",
  True
)

phrase4 = Phrase(
  "Allerede kunde?", 
  "Er du allerede kunde hos oss?",
  "a+shift",
  True
)


# For now a hardcoded dictionary. Later, we I will load this from a JSON file. Should only be combinations of keys that a user ha created (from the allowed hotkey combinations)
# Maybe hotkey_map = load_snippets() from storage folder
hardcoded_testdata = {
  "alt+t": [phrase1, phrase2],  # Example of multiple phrases for the same hotkey
  "a+shift": [phrase3, phrase4],  # Example of multiple phrases for the same hotkey
} 

hotkeys = load_from_file()



def handle_hotkey(hotkey):
  if hotkey in hardcoded_testdata:
    phrases = hardcoded_testdata[hotkey]
    show_popup(phrases)
  else: save_to_file(hardcoded_testdata)# This line should not be in production code



def main():
  start_listener(handle_hotkey)

if __name__ == "__main__":
  main()