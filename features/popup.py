import tkinter as tk

from core.expander import insert_text

def show_popup(phrases):
  root = tk.Tk()
  root.minsize("150", "200")
  root.geometry("250x300")
   
  listbox = tk.Listbox(root)
  listbox.pack(fill=tk.BOTH, expand=True)

  for c, phrase in enumerate(phrases):
    listbox.insert(c, phrase.title)

  
  def on_click(event):
    selection = listbox.curselection()
    if selection:
      index = selection[0]
      phrase = phrases[index]
      root.destroy()  # Close the popup after selection
      insert_text(phrase.content)
      


  def on_hover(event):
    index = listbox.nearest(event.y)
    listbox.selection_clear(0, tk.END)
    listbox.selection_set(index)
  

  def on_close():
    root.destroy()  # Close the popup when the window is closed

  # Clicks outside of popup should close it. Need to implement that
  #def on_click_outside(event):


  # Bind events
  listbox.bind("<Button-1>", on_click)
  listbox.bind("<Motion>", on_hover)
  
  root.attributes("-topmost", True)  # Keep the popup on top of other windows
  #root.focus_force()  # Force focus on the popup window
  root.protocol("WM_DELETE_WINDOW", on_close)  # Handle window close event

  root.mainloop()