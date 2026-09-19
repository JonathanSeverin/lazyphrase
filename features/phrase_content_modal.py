import tkinter as tk


modal = None

def show_modal_content(root, phrase, listbox_element_x, listbox_element_y, width):
  global modal

  if modal: close_content_modal()
  modal = tk.Toplevel(root)
  modal.withdraw()  # Hide the modal initially to prevent flickering, only showing it after setting its position
  modal.overrideredirect(True)  # Remove window decorations

  modal_width = width + (width // 3)

  content_label = tk.Label(modal, text=phrase.content, justify="left", wraplength=modal_width, padx=10, pady=5, anchor="n", )
  content_label.pack()

  modal.update_idletasks()  # Ensure the modal's size is calculated

  modal_x = listbox_element_x # Position the modal to the right of the popup
  modal_y = listbox_element_y # Align the top of the modal with the top of the popup

  modal.geometry(f"+{modal_x}+{modal_y}")  # Set the position of the modal, let the size be determined by its content
  modal.deiconify()  # Show the modal after setting its position


def close_content_modal():
  global modal
  if modal:
    modal.destroy()
    modal = None

