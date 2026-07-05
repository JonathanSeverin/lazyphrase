import tkinter as tk

from core.expander import insert_text



def create_popup(root, phrases, on_popup_close):
  
  toplvl = tk.Toplevel(root)
  toplvl.minsize("150", "200")
  toplvl.geometry("250x300")
  print("Creating new popup")
  current_popup = toplvl  # Set the current popup to the new window
   
  listbox = tk.Listbox(toplvl)
  listbox.pack(fill=tk.BOTH, expand=True)

  for c, phrase in enumerate(phrases):
    listbox.insert(c, phrase.title)

  listbox.focus_set()  # Set focus to the listbox so it can receive keyboard events

  
  def on_click(event):
    selection = listbox.curselection()
    if selection:
      index = selection[0]
      phrase = phrases[index]
      on_popup_close()
      insert_text(phrase.content)
      

  def on_hover(event):
    index = listbox.nearest(event.y)
    listbox.selection_clear(0, tk.END)
    listbox.selection_set(index)
  

  def on_arrow_key_pressed(event):
    selection = listbox.curselection()
    if selection:
      index = selection[0]
      if event.keysym == "Up" and index > 0:
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(index - 1)
      elif (event.keysym == "Down") and ((index + 1) < listbox.size()):
        listbox.selection_clear(0, tk.END)
        listbox.selection_set(index + 1)


  def on_close():
    on_popup_close() 

  def check_focus():
    if toplvl.focus_displayof() is None:
      on_popup_close()  

  # Bind events
  listbox.bind("<Button-1>", on_click)
  listbox.bind("<Return>", on_click)  # Bind Enter key to selection
  listbox.bind("<Motion>", on_hover)
  listbox.bind("Up", on_arrow_key_pressed)
  listbox.bind("Down", on_arrow_key_pressed)
  toplvl.bind("<FocusOut>", lambda event: toplvl.after(100, check_focus))  # Close the popup when it loses focus



  toplvl.attributes("-topmost", True)  # Keep the popup on top of other windows
  toplvl.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close event

