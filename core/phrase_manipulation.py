def add_phrase(title, content, hotkey, is_active):
  pass


def delete_phrase():
  pass

def edit_phrase():
  pass



def filter_phrases(phrases, query):
  return [p for p in phrases if query in p.title.lower()]
