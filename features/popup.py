import tkinter as tk

from core.expander import insert_text

def show_popup(phrases):
  root = tk.Tk()
  root.minsize("150", "200")
  root.geometry("250x300")
   
  listbox = tk.Listbox(root)

  for c, phrase in enumerate(phrases):
    listbox.insert(c, phrase.title)

  
  def on_click(event):
    selection = listbox.curselection()
    if selection:
      index = selection[0]
      phrase = phrases[index]
      insert_text(phrase.content)
      root.destroy()  # Close the popup after selection


  def on_hover(event):
    index = listbox.nearest(event.y)
    listbox.selection_clear(0, tk.END)
    listbox.selection_set(index)
  

  # Clicks outside of popup should close it. Need to implement that
  def on_close():
    root.destroy()  # Close the popup when the window is closed




  listbox.bind("<Button-1>", on_click)
  listbox.bind("<Motion>", on_hover)


  listbox.pack(fill=tk.BOTH, expand=True)
  root.mainloop()


""" 
skjønne koden
fikse display av koden, ser helt ass ut
fikse hvorfor den ikke limer inn andre steder enn i terminal nå
 """