## Main UI window for managing phrases
from operator import index
import tkinter as tk
import uuid
from core.phrase_manipulation import filter_phrases
from models.phrase import Phrase
from storage.file_store import save_phrases, load_phrases
  

phrase_manager_window = None
root = None
phrases = None
clicked_phrase = None # holds the index of the clicked phrase
pending_search = None 
displayed_phrases = None

HOTKEY_KEY_ALIASES = {
  "+": "plus",
  "\\": "backslash",
  ".": "period",
  ",": "comma",
  "-": "minus",
  "<": "less",
  "'": "apostrophe",
}

HOTKEY_DISPLAY_ALIASES = {value: key for key, value in HOTKEY_KEY_ALIASES.items()}

def init_phrase_manager(main_root):
  global phrase_manager_window
  global root
  global phrases
  global displayed_phrases

  root = main_root
  phrases = load_phrases()  
  displayed_phrases = []

  phrase_manager_window = tk.Toplevel(main_root)
  phrase_manager_window.title("Phrase Manager")
  phrase_manager_window.geometry("800x500") # Should probably make it more dynamic based on screen size


  topbar = tk.Frame(phrase_manager_window)
  topbar.pack(side=tk.TOP, fill=tk.X)

  create_button = tk.Button(topbar, text="Create Phrase", command=lambda: print("Create Phrase clicked"))
  create_button.pack(side=tk.LEFT, padx=5, pady=5)
  
  import_button = tk.Button(topbar, text="Import Phrases", command=lambda: print("Import Phrases clicked"))
  import_button.pack(side=tk.LEFT, padx=5, pady=5)


  leftframe = tk.Frame(phrase_manager_window, width=260)
  leftframe.pack(side=tk.LEFT, fill=tk.Y)
  leftframe.pack_propagate(False)  # Prevent the left frame from resizing based on its content

  search_label = tk.Label(leftframe, text="Search:")
  search_label.pack(side=tk.TOP, padx=5, pady=5)
  
  search_label_entry = tk.Entry(leftframe)
  search_label_entry.pack(side=tk.TOP, padx=5, pady=5)

  listbox = tk.Listbox(leftframe)
  listbox.pack(fill=tk.BOTH, expand=True)

  for p in phrases:
    listbox.insert(tk.END, p.title)
    displayed_phrases.append(p)

  
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


 



  # Functions

  def on_phrase_selected(event):
    global clicked_phrase

    selection = listbox.curselection()
    if not selection:
      return

    new_index = selection[0]
    new_phrase = displayed_phrases[new_index]

    if (clicked_phrase is not None) and (clicked_phrase is not new_phrase):
      if save_phrase_validation(event):
        save_phrase()
      else:
        print("Could not save phrases") # again -> popup window or standard error message fro not beeing able to save

    clicked_phrase = new_phrase
    load_prases_into_fields(clicked_phrase)
   
    


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


  def on_inputfields_focus_out(event):
    if save_phrase_validation(event):
      save_phrase()
      load_prases_into_fields(clicked_phrase)
    else:
      print("Could not save phrases") # again -> popup window or standard error message fro not beeing able to save


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
    displayed_phrases.append(newPhrase)

    # give this phrase focus in the listbox
    listbox.insert(tk.END, newPhrase.title)
    listbox.selection_set(tk.END)
    clicked_phrase = displayed_phrases[listbox.size() - 1]

    load_prases_into_fields(clicked_phrase)
    
    if save_phrase_validation(None):
      save_phrases(phrases)
    else:
      print("Phrase not saved due to validation errors.")
      # Should dispalay a message box or some other form of feedback to the user instead of just printing to console. Should be coordinated with the validation function to display the specific error message.

  
  def load_prases_into_fields(phrase):
    phrase_title_entry.delete(0, tk.END)
    phrase_title_entry.insert(0, phrase.title)

    phrase_content_text.delete("1.0", tk.END)
    phrase_content_text.insert(tk.END, phrase.content)

    hotkey_entry.delete(0, tk.END)
    hotkey_entry.insert(0, extract_hotkey_key(phrase.hotkey))


  def save_phrase():
    phrase = clicked_phrase

    if phrase in displayed_phrases:
      index = displayed_phrases.index(phrase)
      listbox.delete(index)
      listbox.insert(index, phrase_title_entry.get() if phrase_title_entry.get() else "New Phrase") # If the title is empty, set it to "New Phrase"
  
    phrase.title = phrase_title_entry.get() if phrase_title_entry.get() else "New Phrase" # If the title is empty, update the phrase title itsle, not just the listbox entry"
    phrase.content = phrase_content_text.get("1.0", tk.END).strip()
    phrase.hotkey = build_hotkey_value(hotkey_entry.get())

    save_phrases(phrases)


  def on_delete_phrase_clicked(event):
    global clicked_phrase

    selection = listbox.curselection()
    if not selection:
      return

    index = selection[0]
    phrase_to_delete = displayed_phrases[index]
    del displayed_phrases[index]
    del phrases[phrases.index(phrase_to_delete)]
    listbox.delete(index)

    size = listbox.size()
    if size == 0:
      clicked_phrase = None
      phrase_title_entry.delete(0, tk.END)
      phrase_content_text.delete("1.0", tk.END)
      hotkey_entry.delete(0, tk.END)
    else:
      new_index = index if index < size else size - 1
      listbox.selection_set(new_index)
      clicked_phrase = displayed_phrases[new_index]
      load_prases_into_fields(clicked_phrase)


  def on_search_key(event):
    global pending_search
    if pending_search is not None:
      root.after_cancel(pending_search)
    pending_search = root.after(200, apply_search)

    
  def apply_search():
    global displayed_phrases
    
    if not phrases:
      return 
    
    if not search_label_entry.get():
      listbox.delete(0, tk.END)
      for p in phrases:
        listbox.insert(tk.END, p.title)
      return

    search_term = search_label_entry.get().lower()
    displayed_phrases = filter_phrases(phrases, search_term)
    listbox.delete(0, tk.END)
    for p in displayed_phrases:
      listbox.insert(tk.END, p.title)



  # Bindings
  listbox.bind("<<ListboxSelect>>", on_phrase_selected)  
  create_button.bind("<Button-1>", on_create_phrase_clicked)
  delete_button.bind("<Button-1>", on_delete_phrase_clicked)
  phrase_title_entry.bind("<FocusOut>", on_inputfields_focus_out)
  phrase_content_text.bind("<FocusOut>", on_inputfields_focus_out)
  hotkey_entry.bind("<FocusOut>", on_inputfields_focus_out)
  search_label_entry.bind("<KeyRelease>", on_search_key)

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


def normalize_hotkey_key(key_text):
  if not key_text:
    return ""

  return HOTKEY_KEY_ALIASES.get(key_text.strip().lower(), key_text.strip().lower())


def display_hotkey_key(key_name):
  if not key_name:
    return ""

  return HOTKEY_DISPLAY_ALIASES.get(key_name, key_name)


def build_hotkey_value(key_text):
  normalized_key = normalize_hotkey_key(key_text)
  if not normalized_key:
    return None

  return f"alt+{normalized_key}"


def extract_hotkey_key(hotkey):
  if not hotkey:
    return ""

  parts = [part.strip().lower() for part in hotkey.split("+")]
  if len(parts) < 2:
    return ""

  modifiers = []
  key_parts = []

  for part in parts:
    if key_parts:
      key_parts.append(part)
      continue

    if part in ("ctrl", "alt", "shift", "cmd", "win"):
      modifiers.append(part)
    else:
      key_parts.append(part)

  if not modifiers or not key_parts:
    return ""

  return display_hotkey_key(normalize_hotkey_key("+".join(key_parts).strip()))


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
  try:
    save_phrases(phrases)
  except Exception as e:
    print(f"Could not save phrases: {e}")
  root.destroy()  