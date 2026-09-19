# Lazyphrase

A lightweight, hotkey-driven text expander for Linux, built with Python and Tkinter.

Press a hotkey, pick a saved phrase from a popup, and it's typed into whatever application has focus. No clipboard managers, no context switching.

## Why this exists

At my part time job I rely heavily on [PhraseExpress](https://www.phraseexpress.com/) for text expansion. When I switched my home office desktop to Linux, I found PhraseExpress doesn't run there, and there was no lightweight equivalent I was happy with. So I built a lightweight version, and used it as an opportunity to dig a bit into system-level programming.

## Features

- **Global hotkeys** — bind any `Alt` + key combination to one or more phrases.
- **Popup phrase picker** — if a hotkey has multiple phrases attached, a small popup lets you pick one, with a live preview of its content on hover.
- **Direct insertion** — if a hotkey maps to a single phrase, it's inserted immediately with no popup.
- **Phrase manager UI** — create, edit, delete, and search phrases in a dedicated window.
- **Import phrase lists** — load a phrase collection from any JSON file on disk.
- **Persistent storage** — phrases are saved locally as JSON (`~/.local/share/phraseexpander/phrases.json`).

## How it works

1. A background listener grabs your configured hotkeys at the X11 level (with a `pynput`-based fallback if that's unavailable).
2. When a hotkey fires, the matching phrase(s) are looked up.
3. The phrase content is copied to the clipboard and a synthetic `Ctrl+V` is sent to the focused window, after which your original clipboard contents are restored.

## Requirements

- **Linux**, running an **X11** session (not Wayland).
- Python 3.10+
- `xclip` or `xsel` installed, for clipboard access via `pyperclip`:
  ```bash
  sudo apt install xclip
  ```

### A note on X11

This project depends on X11 for two things Wayland deliberately restricts for security reasons: global hotkey listening and synthetic keystroke injection. X11 has no security boundary between applications, so any app (this one included) can read input from and inject input into any other window. It's also why there's no straightforward equivalent of this app for Wayland today.

Since most modern distros now default to Wayland, you'll need to explicitly select an X11/"on Xorg" session from your login screen to try this out. If you don't want to touch your main setup at all, running it inside a VM with an X11-based desktop is the safest way to test it out.

## Installation

```bash
git clone https://github.com/JonathanSeverin/phrase-expander.git
cd phrase-expander

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

## Running

```bash
python3 main.py
```

On first launch, the main window appears:

- **Phrase Manager** — where you create and edit phrases. You can minimize this so it only runs in the background.


### Creating a phrase

1. Click **Create Phrase** in the Phrase Manager.
2. Fill in a title and the text content you want inserted.
3. Set a hotkey key (combined with `Alt`, e.g. entering `q` binds `Alt+Q`).
4. Click away from the field to save. Changes save automatically on focus loss.

### Using a phrase

Press the configured hotkey anywhere on your system:

- If it's the only phrase on that hotkey, it's typed out immediately.
- If multiple phrases share the hotkey, a small popup appears. Hover over it to preview, click (or press Enter) to insert.

## Project structure

```
main.py                       # Entry point: wires up the listener and manager windows
core/
  hotkeys.py                  # X11 / pynput global hotkey listener
  expander.py                 # Clipboard-based text insertion
  phrase_manipulation.py      # Validation and hotkey/phrase helpers
features/
  phrase_manager.py           # Phrase Manager UI (create/edit/delete/search/import)
  popup.py                    # Hotkey-triggered phrase picker popup
  popup_manager.py            # Popup lifecycle and single-phrase direct insertion
  phrase_content_modal.py     # Hover preview tooltip
models/
  phrase.py                   # Phrase data model
storage/
  file_store.py               # JSON persistence and file import dialog
```

## Some Known limitations

This is an (somewhat) actively evolving personal project, not a polished product by any means. A few known rough edges:

- Phrases created while the app is running aren't yet picked up by the hotkey listener without a restart.
- Validation errors currently print to the console rather than surfacing in the UI.
