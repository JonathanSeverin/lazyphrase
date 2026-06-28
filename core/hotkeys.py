from pynput import keyboard


def build_hotkey_string(current_keys):
  elements = list(current_keys)
  elements.sort() # ensures consistent order for the hotkey string (since sets are unordered and could lead to different strings for the same hotkey combination)
  return "+".join(elements)


def normalize_key(key):
  try:
    if key.char: return str(key.char).lower()
  except AttributeError:
    pass
  return str(key).replace("Key.", "")


def start_listener(on_hotkey):

  current_keys = set()

  def on_press(key):
    current_keys.add(normalize_key(key))
    if len(current_keys) > 1:
      hotkey_string = build_hotkey_string(current_keys) 
      on_hotkey(hotkey_string)
    

  def on_release(key):
    current_keys.discard(normalize_key(key))
    if key == keyboard.Key.esc:
      # Stop listener
      return False
      ## Just for testing. Should not stop the listener in production code.


  listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release
  )
  listener.start()
  listener.join()

