from pynput import keyboard


def build_hotkey_string(current_keys):
  elements = list(current_keys)
  elements.sort() # ensures consistent order for the hotkey string (since sets are unordered and could lead to different strings for the same hotkey combination)
  return "+".join(elements)


def normalize_key(key):
  temp = None

  try:
    if key.char: return str(key.char).lower()
  except AttributeError:
    pass

  lst = str(key).split(".")
  if len(lst) > 1 and lst[0] == "Key": 
    temp = lst[1]

    if temp.endswith("_l") or temp.endswith("_r"):
      temp = temp[:-2]  # Remove the "_l" or "_r" ending

  return temp.lower() if temp else str(key).lower() 


def start_listener(on_hotkey):

  current_keys = set()
  last_hotkey = None

  def on_press(key):
      nonlocal last_hotkey

      current_keys.add(normalize_key(key))

      if len(current_keys) > 1:
        hotkey_string = build_hotkey_string(current_keys) 

        if hotkey_string != last_hotkey:
          on_hotkey(hotkey_string)
          last_hotkey = hotkey_string
          current_keys.clear()  # Clear the set after triggering the hotkey. See note 1 at end of file for explanation
  

  def on_release(key):
    nonlocal last_hotkey

    current_keys.discard(normalize_key(key))
    if not current_keys: last_hotkey = None

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


"""  
Note1: Some key combinations (e.g. Ctrl+S) may behave differently when the program
is run inside a terminal. In many Unix-like systems, Ctrl+S is used for flow control
(XOFF), which pauses terminal input/output. 
Press Ctrl+Q to resume.

Additionally, current_keys is cleared after a hotkey is triggered to ensure a clean
state and avoid issues if key release events are missed by the system.
Extra layer in additon to on_release to ensure that current_keys is cleared after a hotkey is triggered.
This is to avoid issues if key release events are missed by the system.
"""
