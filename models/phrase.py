class Phrase: 
  def __init__(self, title, content, hotkey=None, is_active=True):
    self.title = title
    self.content = content
    self.hotkey = hotkey
    self.is_active = is_active