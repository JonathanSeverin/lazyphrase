import tkinter as tk

from features.popup import create_popup


root = None
top_level_popup = None  # Global variable to keep track of the current popup window

def init_popup_manager():
    global root
    root = tk.Tk()
    # root.withdraw()  # Hide the main window
    return root  # Return the root window for further use if needed




def request_popup(phrases):
    # blabla
    global top_level_popup
    top_level_popup = create_popup(root, phrases, on_popup_close)  # Call the function to create the popup window
    top_level_popup.mainloop()  # Start the main loop for the popup window


def on_popup_close():
    global top_level_popup
    if top_level_popup is not None:
        top_level_popup.destroy()  
        top_level_popup = None  
