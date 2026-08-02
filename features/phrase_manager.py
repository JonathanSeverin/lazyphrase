## Main UI window for managing phrases
from operator import index
import tkinter as tk
import uuid
from models.phrase import Phrase
from storage.file_store import save_phrases, load_phrases
  

phrase_manager_window = None
root = None
phrases = None
clicked_phrase = None # holds the index of the clicked phrase

def init_phrase_manager(main_root):
  global phrase_manager_window
  global root
  global phrases

  

  root = main_root
  phrases = load_phrases()  

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

  for p in phrases:
    listbox.insert(tk.END, p.title)


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



  char_button = tk.Button(hotkeyframe, text="Alt")
  char_button.pack(side=tk.LEFT, padx=5, pady=5)

  hotkey_label = tk.Label(hotkeyframe, text="Key:")
  hotkey_label.pack(side=tk.LEFT, padx=5, pady=5)

  hotkey_entry = tk.Entry(hotkeyframe, width=6)
  hotkey_entry.pack(side=tk.LEFT)

  delete_button = tk.Button(actionframe, text="Delete", command=lambda: print("Delete clicked"))
  delete_button.pack(side=tk.LEFT, padx=5, pady=5)


  create_button = tk.Button(topbar, text="Create Phrase", command=lambda: print("Create Phrase clicked"))
  create_button.pack(side=tk.LEFT, padx=5, pady=5)

  import_button = tk.Button(topbar, text="Import Phrases", command=lambda: print("Import Phrases clicked"))
  import_button.pack(side=tk.LEFT, padx=5, pady=5)




  # Functions

  def on_phrase_selected(event):
    selection = listbox.curselection()
    if not selection:
      return
    load_prases_into_fileds(selection[0])
   

  def on_phrase_clicked(event):
    global clicked_phrase
    selection = listbox.curselection()
    if selection:
      clicked_phrase = selection[0]


  def save_phrase_validation(event):
    v_title = validate_phrase_title(phrase_title_entry.get())
    v_content = validate_phrase_content(phrase_content_text.get("1.0", tk.END).strip())
    v_hotkey = validate_hotkey(hotkey_entry.get())

    if all([v_title, v_content, v_hotkey]):
      return True
    elif not v_title:
      print("Invalid title. Maximum of 50 characters.")
      return False
    elif not v_content:
      print("Invalid content. Cannot be more than 1000 characters.")
      return False
    elif not v_hotkey:
      print("Invalid hotkey. Please enter a single character for the hotkey.")
      return False
    # Should display a message box or some other form of feedback to the user instead of just printing to console.


  def on_create_phrase_clicked(event):
    global clicked_phrase

    newPhrase = Phrase(
      title="New Phrase",
      content="",
      hotkey="alt+a", # Should improve to be an empty string as default, but the normalization is not implemented for that as of now. Only takes last char as key no matter what it is
      id=str(uuid.uuid4()),
      is_active=True
    )
    phrases.append(newPhrase)

    # give this phrase focus in the listbox
    listbox.insert(tk.END, newPhrase.title)
    listbox.selection_set(tk.END)
    clicked_phrase = listbox.size() - 1

    load_prases_into_fileds(clicked_phrase)
    
    if save_phrase_validation(None):
      save_phrases(phrases)
    else:
      print("Phrase not saved due to validation errors.")
      # Should dispalay a message box or some other form of feedback to the user instead of just printing to console. Should be coordinated with the validation function to display the specific error message.

  
  def load_prases_into_fileds(index):
    phrase = phrases[index]
    
    phrase_title_entry.delete(0, tk.END)
    phrase_title_entry.insert(0, phrase.title)

    phrase_content_text.delete("1.0", tk.END)
    phrase_content_text.insert(tk.END, phrase.content)

    hotkey_entry.delete(0, tk.END)
    hotkey_entry.insert(0, phrase.hotkey[-1]) # This implementation only supports hotkeys of the form "alt+<key>". The key HAS to be ONE char. Hotkeys like "alt+shift+<key>" are not supported. T


  def save_phrase():
    phrase = phrases[clicked_phrase]
    
    listbox.delete(clicked_phrase)
    listbox.insert(clicked_phrase, phrase_title_entry.get())

    phrase.title = phrase_title_entry.get()
    phrase.content = phrase_content_text.get("1.0", tk.END).strip()
    phrase.hotkey = "alt+" + hotkey_entry.get()

    save_phrases(phrases)



  # Bindings
  listbox.bind("<<ListboxSelect>>", on_phrase_clicked)
  listbox.bind("<<ListboxSelect>>", on_phrase_selected, add="+")  # Add the new binding without replacing the existing one
  create_button.bind("<Button-1>", on_create_phrase_clicked)


# on_focus_out for title, content and hotkey should trigger save_phrase_validation and then save the phrase if valid.
# Same goes for on_create_phrase_clicked and on_delete_phrase_clicked. They should validate the phrase before saving or deleting.

  phrase_manager_window.protocol(
    "WM_DELETE_WINDOW", 
    on_close
  )


def validate_hotkey(hotkey):
  if len(hotkey) > 1:
    return False
  return True


def validate_phrase_title(title):
  if len(title) > 50:
    return False
  return True


def validate_phrase_content(content):
  if len(content) > 1000:
    return False
  return True


def convert_to_phrase_dict(phrase_list):
  out_dict = {}
  for p in phrase_list:
    if p.hotkey in out_dict: out_dict[p.hotkey].append(p)
    else: out_dict[p.hotkey] = [p]
  return out_dict


def show_phrase_manager(): # not used as of now
  global phrase_manager_window
  if phrase_manager_window is not None:
    phrase_manager_window.deiconify()  # Show the window
    phrase_manager_window.lift()  
    phrase_manager_window.focus_force()  


def get_phrases_dict():
  phrase_dict = convert_to_phrase_dict(phrases)
  if not phrase_dict:
    return {}
  return phrase_dict


# Close the main application window, and further the whole application
def on_close():
  root.destroy()  