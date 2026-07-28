## Main UI window for managing phrases
from operator import index
import tkinter as tk
from storage.file_store import save_to_file, load_from_file
  

phrase_manager_window = None
root = None
phrases = None

def init_phrase_manager(main_root):
  global phrase_manager_window
  global root
  global phrases

  root = main_root
  phrases = load_from_file()  

  phrase_manager_window = tk.Toplevel(main_root)
  phrase_manager_window.title("Phrase Manager")
  phrase_manager_window.geometry("800x500") # Should probably make it more dynamic based on screen size

  topbar = tk.Frame(phrase_manager_window)
  topbar.pack(side=tk.TOP, fill=tk.X)

  leftframe = tk.Frame(phrase_manager_window, width=260)
  leftframe.pack(side=tk.LEFT, fill=tk.Y)
  leftframe.pack_propagate(False)  # Prevent the left frame from resizing based on its content

  listbox = tk.Listbox(leftframe)
  listbox.pack(fill=tk.BOTH, expand=True)

  for p in phrases.values():
    for phrase in p:
      listbox.insert(tk.END, phrase.title)


  rightframe = tk.Frame(phrase_manager_window)
  rightframe.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

  titleframe = tk.Frame(rightframe)
  titleframe.pack(side=tk.TOP, fill=tk.X)

  bottomframe = tk.Frame(rightframe)
  bottomframe.pack(side=tk.BOTTOM, fill=tk.X)

  contentframe = tk.Frame(rightframe)
  contentframe.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

  hotkeyframe = tk.Frame(bottomframe)
  hotkeyframe.pack(side=tk.LEFT, fill=tk.X, expand=True)

  actionframe = tk.Frame(bottomframe)
  actionframe.pack(side=tk.RIGHT, fill=tk.X)


  phrase_title_label = tk.Label(titleframe, text="Phrase Title:")
  phrase_title_label.pack(side=tk.LEFT, padx=5, pady=5)

  phrase_title_entry = tk.Entry(titleframe)
  phrase_title_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, pady=5)

  phrase_content_label = tk.Label(contentframe, text="Phrase Content:")
  phrase_content_label.pack(side=tk.TOP, anchor="w", padx=5, pady=5)

  phrase_content_text = tk.Text(contentframe)
  phrase_content_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)



  char_button = tk.Button(hotkeyframe, text="Set Hotkey", command=lambda: print("Set Hotkey clicked"))
  char_button.pack(side=tk.LEFT, padx=5, pady=5)

  hotkey_button = tk.Button(hotkeyframe, text="Set Hotkey", command=lambda: print("Set Hotkey clicked"))
  hotkey_button.pack(side=tk.LEFT, padx=5, pady=5)

  save_button = tk.Button(actionframe, text="Save", command=lambda: print("Save clicked"))
  save_button.pack(side=tk.LEFT, padx=5, pady=5)

  delete_button = tk.Button(actionframe, text="Delete", command=lambda: print("Delete clicked"))
  delete_button.pack(side=tk.LEFT, padx=5, pady=5)


  create_button = tk.Button(topbar, text="Create Phrase", command=lambda: print("Create Phrase clicked"))
  create_button.pack(side=tk.LEFT, padx=5, pady=5)

  import_button = tk.Button(topbar, text="Import Phrases", command=lambda: print("Import Phrases clicked"))
  import_button.pack(side=tk.LEFT, padx=5, pady=5)



  # Bindings

  




  # Functions

  def on_phrase_selected(event):
    selection = listbox.curselection()
    if not selection:
     return

    index = selection[0]
    phrase = phrases[index]

    phrase_title_entry.delete(0, tk.END)
    phrase_title_entry.insert(0, phrase.title)

    phrase_content_text.delete("1.0", tk.END)
    phrase_content_text.insert(tk.END, phrase.content)


  listbox.bind("<<ListboxSelect>>", on_phrase_selected)







  phrase_manager_window.protocol(
    "WM_DELETE_WINDOW", 
    on_close
  )




def show_phrase_manager(): # not used as of now
  global phrase_manager_window
  if phrase_manager_window is not None:
    phrase_manager_window.deiconify()  # Show the window
    phrase_manager_window.lift()  
    phrase_manager_window.focus_force()  


# Close the main application window, and further the whole application
def on_close():
  root.destroy()  