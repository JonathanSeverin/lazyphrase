## Main UI window for managing phrases
import tkinter as tk
  

phrase_manager_window = None

def init_phrase_manager(main_root):
  global phrase_manager_window

  phrase_manager_window = tk.Toplevel(main_root)
  phrase_manager_window.title("Phrase Manager")
  phrase_manager_window.geometry("800x500") # Should probably make it more dynamic based on screen size

  topbar = tk.Frame(phrase_manager_window)
  topbar.pack(side=tk.TOP, fill=tk.X)

  listbox = tk.Listbox(phrase_manager_window)
  listbox.pack(fill=tk.BOTH, expand=False)



  create_button = tk.Button(phrase_manager_window, text="Create Phrase", command=lambda: print("Create Phrase clicked"))
  create_button.pack(side=tk.LEFT, padx=5, pady=5)




def show_phrase_manager():
  global phrase_manager_window
  if phrase_manager_window is not None:
    phrase_manager_window.deiconify()  # Show the window
    phrase_manager_window.lift()  
    phrase_manager_window.focus_force()  
  
