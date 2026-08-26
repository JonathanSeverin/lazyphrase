import tkinter as tk


modal = None

def show_modal_content(root, phrase, popup_geometry):
  global modal

  if modal: close_content_modal()
  modal = tk.Toplevel(root)
  modal.overrideredirect(True)  # Remove window decorations

  width, height, x, y = parse_geometry(popup_geometry)
  modal_width = width + (width // 3)

  content_label = tk.Label(modal, text=phrase.content, justify="left", wraplength=modal_width, padx=10, pady=5, anchor="n", )
  content_label.pack()

  modal.update_idletasks()  # Ensure the modal's size is calculated

  modal_x = x + width + 15  # Position the modal to the right of the popup
  modal_y = y # Align the top of the modal with the top of the popup

  modal.geometry(f"+{modal_x}+{modal_y}")  # Set the position of the modal, let the size be determined by its content


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