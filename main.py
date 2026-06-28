from core.hotkeys import start_listener

# For now a hardcoded dictionary. Later, we I will load this from a JSON file. Should only be combinations of keys that a user ha created (from the allowed hotkey combinations)
# Maybe hotkey_map = load_snippets() from storage folder
hotkeys = {
  "alt+q": lambda: print("Hello, this is a test snippet for alt+q"),
  "ctrl+s": lambda: print("This is another test snippet for ctrl+s"),
  "shift+r": lambda: print("This is another test snippet for shift+r"),
  "r+shift": lambda: print("This is another test snippet for r+shift"),
  "ctrl+g": lambda: print("This is another test snippet for ctrl+g"),
} 


def handle_hotkey(hotkey):
  if hotkey in hotkeys:
    action = hotkeys.get(hotkey)
    if action: action()
  else: print(hotkey)

def main():
  start_listener(handle_hotkey)


if __name__ == "__main__":
  main()