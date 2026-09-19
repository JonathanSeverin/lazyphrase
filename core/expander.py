import threading
import pyperclip
from pynput.keyboard import Controller, Key

from features.phrase_content_modal import close_content_modal

keyboard = Controller()

def insert_text(text):
  original_clipboard = preserve_clipboard()

  pyperclip.copy(text)
  keyboard.press(Key.ctrl)
  keyboard.press('v')
  keyboard.release('v')
  keyboard.release(Key.ctrl)

  close_content_modal()  # Close the modal after inserting the text
  
  def restore():
    pyperclip.copy(original_clipboard)

  threading.Timer(0.15, restore).start() # Increase delay if necessary


def preserve_clipboard():
  original_clipboard = pyperclip.paste()
  return original_clipboard