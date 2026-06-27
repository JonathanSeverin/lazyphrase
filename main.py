from core.hotkeys import start_listener

hotkeys = {} # Unsure if this should be in main or in hotkeys. Should be loaded from a config file. 
# For now, just hardcoding it here. If user has not defined any hotkeys, this will be empty. 

# Maybe hotkey_map = load_snippets() from storage folder





def main():
  start_listener()


if __name__ == "__main__":
  main()