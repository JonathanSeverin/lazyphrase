## Main UI window for managing phrases
import tkinter as tk
  

def show_phrase_manager(root):
  root = tk.Tk() # NB, should only have one root in the entire application, so this should be refactored to use the existing root from popup_manager.py
  root.title("Phrase Manager")
  root.geometry("400x300")
