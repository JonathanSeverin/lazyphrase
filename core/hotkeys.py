from pynput import keyboard

current_keys = set()

def on_press(key):
  current_keys.add(key)
  try:
    print(f'alphanumeric key {key.char} pressed')
  except AttributeError:
    print(f'special key {key} pressed')


def on_release(key):
  current_keys.discard(key)
  print(f'{key} released')
  if key == keyboard.Key.esc:
    # Stop listener
    return False
    ## Just for testing. Should not stop the listener in production code.

def build_hotkey_string():
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


def start_listener():
  listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release
  )
  listener.start()
  listener.join()

