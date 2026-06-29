from core.hotkeys import start_listener
from models.phrase import Phrase

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
hotkeys = {
  "alt+t": [phrase1, phrase2],  # Example of multiple phrases for the same hotkey
  "a+shift": [phrase3, phrase4],  # Example of multiple phrases for the same hotkey
} 

def show_popup(phrases):
  for i, p in enumerate(phrases):
    print(f"{i+1}. {p.title}")

def handle_hotkey(hotkey):
  if hotkey in hotkeys:
    phrases = hotkeys[hotkey]
    show_popup(phrases)
  else: print(hotkey) # This line should not be in production code



def main():
  start_listener(handle_hotkey)

if __name__ == "__main__":
  main()