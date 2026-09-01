HOTKEY_KEY_ALIASES = {
  "+": "plus",
  "\\": "backslash",
  ".": "period",
  ",": "comma",
  "-": "minus",
  "<": "less",
  "'": "apostrophe",
}

HOTKEY_DISPLAY_ALIASES = {value: key for key, value in HOTKEY_KEY_ALIASES.items()}


def filter_phrases(phrases, query):
  return [p for p in phrases if query in p.title.lower()]

def validate_hotkey(hotkey):
  if len(hotkey) > 1:
    return False
  return True


def normalize_hotkey_key(key_text):
  if not key_text:
    return ""

  return HOTKEY_KEY_ALIASES.get(key_text.strip().lower(), key_text.strip().lower())


def display_hotkey_key(key_name):
  if not key_name:
    return ""

  return HOTKEY_DISPLAY_ALIASES.get(key_name, key_name)


def build_hotkey_value(key_text):
  normalized_key = normalize_hotkey_key(key_text)
  if not normalized_key:
    return None

  return f"alt+{normalized_key}"


def extract_hotkey_key(hotkey):
  if not hotkey:
    return ""

  parts = [part.strip().lower() for part in hotkey.split("+")]
  if len(parts) < 2:
    return ""

  modifiers = []
  key_parts = []

  for part in parts:
    if key_parts:
      key_parts.append(part)
      continue

    if part in ("ctrl", "alt", "shift", "cmd", "win"):
      modifiers.append(part)
    else:
      key_parts.append(part)

  if not modifiers or not key_parts:
    return ""

  return display_hotkey_key(normalize_hotkey_key("+".join(key_parts).strip()))


def validate_phrase_title(title):
  if len(title) > 50:
    return False
  return True


def validate_phrase_content(content):
  if len(content) > 1000:
    return False
  return True


def convert_to_phrase_dict(phrase_list):
  out_dict = {}
  for p in phrase_list:
    if p.hotkey in out_dict: out_dict[p.hotkey].append(p)
    else: out_dict[p.hotkey] = [p]
  return out_dict
