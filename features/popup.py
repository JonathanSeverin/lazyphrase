import tkinter as tk

from core.expander import insert_text



def create_popup(root, phrases, on_popup_close, on_popup_coordinates_update=None, initial_position=None):
  
  toplvl = tk.Toplevel(root)
  toplvl.minsize(150, 200)
  width = 250
  height = 300
  if initial_position is not None:
    x, y = initial_position
    toplvl.geometry(f"{width}x{height}+{x}+{y}")
  else:
    toplvl.geometry(f"{width}x{height}")
   
  listbox = tk.Listbox(toplvl)
  listbox.pack(fill=tk.BOTH, expand=True)

  pending_coordinates_update = None

  for c, phrase in enumerate(phrases):
    listbox.insert(c, phrase.title)

  listbox.focus_set()  # Set focus to the listbox so it can receive keyboard events

  
  def on_click(event):
    selection = listbox.curselection()
    if selection:
      index = selection[0]
      phrase = phrases[index]
      on_popup_close()
      root.after(50, lambda: insert_text(phrase.content))


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


  def flush_coordinates_update():
    nonlocal pending_coordinates_update

    if on_popup_coordinates_update is not None:
      on_popup_coordinates_update(toplvl.winfo_x(), toplvl.winfo_y())

    pending_coordinates_update = None


  def on_configure(event):
    nonlocal pending_coordinates_update

    if pending_coordinates_update is not None:
      toplvl.after_cancel(pending_coordinates_update)

    pending_coordinates_update = toplvl.after(200, flush_coordinates_update)


  def on_close():
    if pending_coordinates_update is not None:
      toplvl.after_cancel(pending_coordinates_update)
      flush_coordinates_update()
    on_popup_close() 


  # Bind events
  listbox.bind("<Button-1>", on_click)
  listbox.bind("<Return>", on_click)  # Bind Enter key to selection
  listbox.bind("<Escape>", lambda event: on_close())
  listbox.bind("<Motion>", on_hover)
  listbox.bind("Up", on_arrow_key_pressed)
  listbox.bind("Down", on_arrow_key_pressed)
  toplvl.bind("<Configure>", on_configure)


  toplvl.attributes("-topmost", True)  # Keep the popup on top of other windows
  toplvl.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close event

  return toplvl