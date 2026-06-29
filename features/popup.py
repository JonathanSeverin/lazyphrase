import tkinter as tk

def show_popup(phrases):
  root = tk.Tk()
  root.geometry("400x300")
  listbox = tk.Listbox(root)

  for c, phrase in enumerate(phrases):
    listbox.insert(c, phrase.title)

  listbox.pack()
  root.mainloop() # needed? What if not added? If added, how to kill?