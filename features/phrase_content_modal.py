import tkinter as tk


modal = None

def show_modal_content(root, phrase, popup_geometry):
  global modal

  if modal: close_content_modal()
  modal = tk.Toplevel(root)

  width, height, x, y = parse_geometry(popup_geometry)

  content_label = tk.Label(modal, text=phrase.content, justify="left", wraplength=width, padx=10, pady=5)
  content_label.pack()

  modal.geometry(f"{width}x{round(height/2)}+{x+width}+{y}")

def close_content_modal():
  global modal
  if modal:
    modal.destroy()
    modal = None



def parse_geometry(geometry_str):
  """Parse a geometry string of the form 'WIDTHxHEIGHT+X+Y' and return a tuple (width, height, x, y)."""
  try:
    dimensions, position = geometry_str.split('+', 1)
    width, height = map(int, dimensions.split('x'))
    x, y = map(int, position.split('+'))
    return width, height, x, y
  except ValueError:
    raise ValueError(f"Invalid geometry string: {geometry_str}")