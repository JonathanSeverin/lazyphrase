from pynput import keyboard


def build_hotkey_string(current_keys):
  elements = []

  for key in current_keys:
    try:
      char = key.char
      if char:
        elements.append(str(char.lower()))
    except AttributeError:
      lst = str(key).split(".")
      if len(lst) == 2 and lst[0] == "Key": elements.append(lst[1])

  elements.sort() # ensures consistent order for the hotkey string (since sets are unordered and could lead to different strings for the same hotkey combination)
  return "+".join(elements)


def start_listener(on_hotkey):

  current_keys = set()

  def on_press(key):
    current_keys.add(key)
    if len(current_keys) > 1:
      hotkey_string = build_hotkey_string(current_keys) 
      on_hotkey(hotkey_string)
    

  def on_release(key):
    current_keys.discard(key)
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

