import uuid

class Phrase: 
  def __init__(self, title, content, hotkey=None, id=None, is_active=True):
    self.title = title
    self.content = content
    self.hotkey = hotkey
    self.id = id if id is not None else str(uuid.uuid4())
    self.is_active = is_active