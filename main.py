import tkinter as tk

from core.hotkeys import start_listener
from features.popup_manager import init_popup_manager, request_popup
from features.phrase_manager import init_phrase_manager
from models.phrase import Phrase
from storage.file_store import save_phrases, load_phrases
from features.phrase_manager import get_phrases_dict



def handle_hotkey(hotkey):
  all_phrases = get_phrases_dict()
  if hotkey in all_phrases:
    selected_phrases = all_phrases[hotkey]
    request_popup(selected_phrases)



def main():
  root = tk.Tk()
  root.withdraw()  # Hide the main window
  init_phrase_manager(root)  
  init_popup_manager(root)
  start_listener(handle_hotkey)
  root.mainloop()  # Start the Tkinter main loop 

if __name__ == "__main__":
  main()