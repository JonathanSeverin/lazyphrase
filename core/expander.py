import threading
import pyperclip
from pynput.keyboard import Controller, Key

keyboard = Controller()

def insert_text(text):
  original_clipboard = preserve_clipboard()

  pyperclip.copy(text)
  keyboard.press(Key.ctrl)
  keyboard.press('v')
  keyboard.release('v')
  keyboard.release(Key.ctrl)

  def restore():
    pyperclip.copy(original_clipboard)

  threading.Timer(0.15, restore).start() # Increase delay if necessary

def preserve_clipboard():
  original_clipboard = pyperclip.paste()
  return original_clipboard