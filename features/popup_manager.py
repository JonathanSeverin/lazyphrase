import tkinter as tk

from features.popup import show_popup


root = None

def init_popup_manager():
    global root
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    # return root  # Return the root window for further use if needed




def request_popup(phrases):
    """
    Request to show a popup with the given phrases.
    This function is called from the main thread and schedules the popup to be shown in the main thread.
    """
    # Schedule the show_popup function to be called in the main thread
    tk._default_root.after(0, show_popup, phrases)