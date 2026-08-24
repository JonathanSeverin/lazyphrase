from core.expander import insert_text
import tkinter as tk

from features.popup import create_popup


root = None
top_level_popup = None  # Global variable to keep track of the current popup window
popup_geometry = None  # Global variable to store the popup window geometry

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

    if len(phrases) == 1:
        direct_phrase_insertion(phrases[0])  # Directly insert the phrase if there's only one
        return
    top_level_popup = create_popup(
        root,
        phrases,
        on_popup_close,
        on_popup_geometry_update,
        popup_geometry,
    )  # Call the function to create the popup window


def direct_phrase_insertion(phrase):
    global root
    root.after(50, lambda: insert_text(phrase.content))  # Schedule the text insertion in the main thread


def on_popup_geometry_update(geometry):
    global popup_geometry
    popup_geometry = geometry  # Update the global variable with the new popup geometry


def on_popup_close():
    global top_level_popup
    if top_level_popup is not None:
        top_level_popup.destroy()  
        top_level_popup = None  