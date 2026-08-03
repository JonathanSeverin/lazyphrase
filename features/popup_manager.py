import tkinter as tk

from features.popup import create_popup


root = None
top_level_popup = None  # Global variable to keep track of the current popup window
popup_coordinates = None  # Global variable to store the coordinates of the popup window

def init_popup_manager(main_root):
    global root
    root = main_root


def request_popup(phrases):
    root.after(0, process_popup_request, phrases)  # Schedule the popup request to be processed in the main thread


def process_popup_request(phrases):
    global root, top_level_popup
    
    if top_level_popup is not None: # Close the existing popup if it exists
        top_level_popup.destroy() 
        top_level_popup = None

    top_level_popup = create_popup(
        root,
        phrases,
        on_popup_close,
        on_popup_coordinates_update,
        popup_coordinates,
    )  # Call the function to create the popup window


def on_popup_coordinates_update(x, y):
    global popup_coordinates
    popup_coordinates = (x, y)  # Update the global variable with the new coordinates


def on_popup_close():
    global top_level_popup
    if top_level_popup is not None:
        top_level_popup.destroy()  
        top_level_popup = None  