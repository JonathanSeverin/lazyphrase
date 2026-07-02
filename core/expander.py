import pyperclip
from pynput.keyboard import Controller, Key

keyboard = Controller()

def insert_text(text):
  pyperclip.copy(text)
  keyboard.press(Key.ctrl)
  keyboard.press('v')
  keyboard.release('v')
  keyboard.release(Key.ctrl)