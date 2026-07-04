import tkinter as tk
import time
import threading
import sys

from core.expander import insert_text


current_popup = None  # Global variable to keep track of the current popup window


def show_popup(phrases):
  
  global current_popup
  print(f"[{time.time():.3f}] show_popup START thread={threading.current_thread().name} module_id={id(sys.modules[__name__])} current_popup={current_popup}")

  if current_popup is not None:
    print(f"[{time.time():.3f}] Closing existing popup id={id(current_popup)}")
    current_popup.destroy()  # Close the existing popup if it exists

  root = tk.Tk()
  root.minsize("150", "200")
  root.geometry("250x300")
  print(f"[{time.time():.3f}] Creating new popup")
  current_popup = root  # Set the current popup to the new window
  print(f"[{time.time():.3f}] created popup id={id(root)} thread={threading.current_thread().name}")
   
  listbox = tk.Listbox(root)
  listbox.pack(fill=tk.BOTH, expand=True)

  for c, phrase in enumerate(phrases):
    listbox.insert(c, phrase.title)

  listbox.focus_set()  # Set focus to the listbox so it can receive keyboard events

  
  def on_click(event):
    selection = listbox.curselection()
    if selection:
      index = selection[0]
      phrase = phrases[index]
      global current_popup
      print(f"[{time.time():.3f}] on_click closing popup id={id(root)} thread={threading.current_thread().name}")
      current_popup = None 
      root.destroy() 
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
    global current_popup
    print(f"[{time.time():.3f}] on_close closing popup id={id(root)} thread={threading.current_thread().name}")
    current_popup = None  
    root.destroy()  

  """ def check_focus():
    global current_popup
    if root.focus_displayof() is None:
      current_popup = None
      root.destroy()  """ 

  # Bind events
  listbox.bind("<Button-1>", on_click)
  listbox.bind("<Return>", on_click)  # Bind Enter key to selection
  listbox.bind("<Motion>", on_hover)
  listbox.bind("Up", on_arrow_key_pressed)
  listbox.bind("Down", on_arrow_key_pressed)
  """ root.bind("<FocusOut>", lambda event: root.after(100, check_focus))  """ # Close the popup when it loses focus



  print(f"[{time.time():.3f}] entering mainloop popup id={id(root)}")
  root.attributes("-topmost", True)  # Keep the popup on top of other windows
  root.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close event

  root.mainloop()
  print(f"[{time.time():.3f}] exited mainloop popup id={id(root)} current_popup={current_popup}")