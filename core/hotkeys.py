from pynput import keyboard


def on_press(key):
  try:
    print(f'alphanumeric key {key.char} pressed')
  except AttributeError:
    print(f'special key {key} pressed')



def on_release(key):
  print(f'{key} released')
  if key == keyboard.Key.esc:
    # Stop listener
    return False
    ## Just for testing. Should not stop the listener in production code.


def start_listener():
  listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release
  )
  listener.start()
  listener.join()