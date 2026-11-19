from models import LanguageModel



class Conversation:
  """A chat session between a user and one model."""

  def __init__(self, conversation_id, model: LanguageModel) -> None:
    self.conversation_id= conversation_id
    self.model= model
    self.messages= []

  def send_message(self, prompt: str) -> str:
    """Send a prompt, store both sides of the exchange, return the reply."""
    response= self.model.generate_response(prompt)
    self.messages.append({
        "role": "user",
        "content": prompt
    })
    self.messages.append({
        "role": "assistant",
        "content": response
    })
    return response

  def display_history(self) -> None:
    """Print the full conversation."""
    for message in self.messages:
      print(f"{message['role']}: {message['content']}")
