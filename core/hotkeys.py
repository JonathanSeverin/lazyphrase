import threading

from pynput import keyboard

try:
  from Xlib import X, XK, display
except ImportError:
  X = None
  XK = None
  display = None


MODIFIER_MASKS = {}
IGNORED_STATE_MASKS = 0
KEY_NAME_ALIASES = {
  "+": "plus",
  "\\": "backslash",
  ".": "period",
  ",": "comma",
  "-": "minus",
  "<": "less",
  "'": "apostrophe",
}
DISPLAY_KEY_NAME_ALIASES = {value: key for key, value in KEY_NAME_ALIASES.items()}

if X is not None:
  MODIFIER_MASKS = {
    "ctrl": X.ControlMask,
    "alt": X.Mod1Mask,
    "shift": X.ShiftMask,
    "cmd": X.Mod4Mask,
    "win": X.Mod4Mask,
  }
  IGNORED_STATE_MASKS = X.LockMask | X.Mod2Mask


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
    if key.char:
      return normalize_key_name(str(key.char).lower())
  except AttributeError:
    pass

  lst = str(key).split(".")
  if len(lst) > 1 and lst[0] == "Key":
    temp = lst[1]

    if temp.endswith("_l") or temp.endswith("_r"):
      temp = temp[:-2]

  return normalize_key_name(temp.lower() if temp else str(key).lower())


def normalize_key_name(key_name):
  if not key_name:
    return None

  return KEY_NAME_ALIASES.get(key_name, key_name)


def display_key_name(key_name):
  if not key_name:
    return ""

  return DISPLAY_KEY_NAME_ALIASES.get(key_name, key_name)


def start_listener(on_hotkey, hotkeys=None):
  hotkeys = list(hotkeys or [])

  if X is not None and hotkeys:
    try:
      start_x11_listener(on_hotkey, hotkeys)
      return
    except Exception as exc:
      print(f"Could not start X11 hotkey grabber: {exc}")
      print("Falling back to pynput listener without suppression.")

  start_fallback_listener(on_hotkey)


def start_x11_listener(on_hotkey, hotkeys):
  x_display = display.Display()
  root = x_display.screen().root

  hotkey_lookup = set()
  grabbed_keycodes = set()

  for hotkey in hotkeys:
    normalized_hotkey = normalize_hotkey(hotkey)
    if normalized_hotkey is None:
      continue

    modifiers, key_name = parse_hotkey(normalized_hotkey)
    if modifiers is None:
      continue

    keycode = keycode_for_key_name(x_display, key_name)
    if keycode is None:
      continue

    hotkey_lookup.add(normalized_hotkey)
    grabbed_keycodes.add(keycode)

    modifier_mask = 0
    for modifier in modifiers:
      modifier_mask |= MODIFIER_MASKS[modifier]

    for ignored_mask in (0, IGNORED_STATE_MASKS):
      root.grab_key(
        keycode,
        modifier_mask | ignored_mask,
        True,
        X.GrabModeAsync,
        X.GrabModeAsync,
      )

  x_display.sync()

  def event_loop():
    last_hotkey = None

    while True:
      event = x_display.next_event()

      if event.type == X.KeyPress:
        if event.detail not in grabbed_keycodes:
          continue

        hotkey = hotkey_from_event(x_display, event)
        if hotkey in hotkey_lookup and hotkey != last_hotkey:
          on_hotkey(hotkey)
          last_hotkey = hotkey

      elif event.type == X.KeyRelease:
        if event.detail in grabbed_keycodes:
          last_hotkey = None

  threading.Thread(target=event_loop, daemon=True).start()


def start_fallback_listener(on_hotkey):
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
        current_keys.clear()

  def on_release(key):
    nonlocal last_hotkey

    current_keys.discard(normalize_key(key))
    if not current_keys:
      last_hotkey = None

    if key == keyboard.Key.esc:
      return False

  listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release,
  )
  listener.start()


def parse_hotkey(hotkey):
  parts = [part.strip().lower() for part in hotkey.split("+")]
  if len(parts) < 2:
    return None, None

  modifiers = []
  key_parts = []

  for part in parts:
    if key_parts:
      key_parts.append(part)
      continue

    if part in MODIFIER_MASKS:
      modifiers.append(part)
    else:
      key_parts.append(part)

  if not modifiers or not key_parts:
    return None, None

  key_name = normalize_key_name("+".join(key_parts).strip())
  if not key_name:
    return None, None

  for modifier in modifiers:
    if modifier not in MODIFIER_MASKS:
      return None, None

  return modifiers, key_name


def normalize_hotkey(hotkey):
  if not hotkey:
    return None

  modifiers, key_name = parse_hotkey(hotkey)
  if modifiers is None:
    return None

  return "+".join([*modifiers, key_name])


def keycode_for_key_name(x_display, key_name):
  keysym = keysym_for_key_name(key_name)
  if keysym == 0:
    return None

  keycode = x_display.keysym_to_keycode(keysym)
  return keycode or None


def keysym_for_key_name(key_name):
  special_names = {
    "esc": "Escape",
    "enter": "Return",
    "return": "Return",
    "space": "space",
    "tab": "Tab",
    "backspace": "BackSpace",
    "delete": "Delete",
    "insert": "Insert",
    "home": "Home",
    "end": "End",
    "pageup": "Page_Up",
    "pagedown": "Page_Down",
    "up": "Up",
    "down": "Down",
    "left": "Left",
    "right": "Right",
    "æ": "ae",
    "ø": "oslash",
    "å": "aring",
  }

  lookup_name = special_names.get(key_name, key_name)
  return XK.string_to_keysym(lookup_name)


def hotkey_from_event(x_display, event):
  state = event.state & ~IGNORED_STATE_MASKS
  modifiers = []

  if state & X.ControlMask:
    modifiers.append("ctrl")
  if state & X.Mod1Mask:
    modifiers.append("alt")
  if state & X.ShiftMask:
    modifiers.append("shift")
  if state & X.Mod4Mask:
    modifiers.append("win")

  key_sym = x_display.keycode_to_keysym(event.detail, 0)
  key_name = XK.keysym_to_string(key_sym)
  if key_name is None:
    return None

  return "+".join([*modifiers, normalize_key_name(key_name.lower())])
