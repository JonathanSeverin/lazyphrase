from pynput import keyboard


# This function takes a set of currently pressed keys and returns a string representation of the hotkey combination. 
# The keys are sorted in a specific order: modifier keys (ctrl, alt, shift, cmd, win) come first, followed by other keys.
def build_hotkey_string(current_keys):
  modifier_order = {
    "ctrl": 0,
    "alt": 1,
    "shift": 2,
    "cmd": 3,
    "win": 3,
  }

  def sort_key(key_name):
    return (
      0 if key_name in modifier_order else 1,
      modifier_order.get(key_name, 99),
      key_name,
    )

  elements = sorted(current_keys, key=sort_key)
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

"""
Note2: Pressing ctrl+c crashed the program. Should be handled in a proper manner. For now, I will just ignore it.
"""
