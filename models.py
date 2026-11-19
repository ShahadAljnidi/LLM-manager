from abc import ABC, abstractmethod

from tokenizer import Tokenizer
from exceptions import InvalidPromptError
from pricing import PricingPlan


class LoggingMixin:
  def log(self, message: str):
    """print a log message"""
    print(f"[LOG] {message}")


class LanguageModel(ABC):
  """Abstract base class for all language models"""

  total_models= 0
  
  def __init__(self, model_name: str, provider: str, max_tokens: int,
              temperature: float, pricing_plan: PricingPlan):
      self.model_name= model_name
      self.provider= provider
      self.max_tokens= max_tokens
      self.__temperature= temperature
      self.tokenizer = Tokenizer()        #composotion
      self.pricing_plan= pricing_plan     #aggregation

      self.__is_active= True
      LanguageModel.total_models +=1


  @abstractmethod
  def generate_response(self, prompt: str) -> str:
    """Return a simulated response. Must be implemented by subclasses."""

  def validate_prompt(self, prompt: str) ->None:
    """Raise InvalidPromptError if the prompt is not a non-empty string."""
    if not isinstance(prompt, str):
           raise InvalidPromptError('Prompt must be string')
    
    if not prompt.strip():
      raise InvalidPromptError('Prompt cannot be empty')

    if prompt.strip().isdigit():
      raise InvalidPromptError("Prompt cannot be only numbers.")

  def _build_response(self, label: str, prompt: str) -> str:
    self.validate_prompt(prompt)
    tokens= self.tokenizer.count_tokens(prompt)
    return f"{label} response to: {prompt}\nInput tokens: {tokens}"
    
  def display_info(self):
    print(self)

  def calculate_request_cost(self, prompt: str) -> float:
    """Print and return the input cost of `prompt`."""
    tokens= self.tokenizer.count_tokens(prompt)
    cost= self.pricing_plan.calculate_cost(tokens)
    print(f"Input tokens: {tokens}")
    print(f"Request cost: ${cost:.6f}")
    return cost

  @classmethod
  def get_total_models(cls) -> int:
    """Return how many models have been created."""
    return cls.total_models

  @staticmethod
  def validate_temperature(temperature: float) -> bool:
    """Return True if temperature is between 0.0 and 2.0."""
    return 0.0 <= temperature <=2.0

# --properties--
  @property
  def temperature(self) -> float:
    return self.__temperature

  @temperature.setter
  def temperature(self, value: float) -> None:
    if not self.validate_temperature(value):
      raise ValueError ("Temperature must be between 0 and 2")
    self.__temperature= value

  
  @property
  def is_active(self) -> bool:
    return self.__is_active

  @is_active.setter
  def is_active(self, value: bool) -> None:
     if not isinstance(value, bool):
        raise ValueError("is_active must be a boolean.")
     self.__is_active = value


#--magic methods--

  def __str__(self) -> str:
     return (
         f"Model name: {self.model_name}"
         f"Provider: {self.provider}"
         f"Maximum Tokens: {self.max_tokens}"
         f"Temperature: {self.temperature}"
     )
  def __repr__(self) -> str:
    return (
        f"{type(self).__name__}("
        f"model_name='{self.model_name}', "
        f"provider='{self.provider}')"
          )

  def __len__(self) -> int:
    return self.max_tokens

  def __eq__(self, other) -> bool:
    if not isinstance(other, LanguageModel):
      return NotImplemented
    return (self.model_name, self.provider) == (other.model_name, other.provider)




class GPTModel(LanguageModel, LoggingMixin):
  def __init__(self, model_name, provider: str, max_tokens: int,
               temperature: float, api_key: str, 
               pricing_plan: PricingPlan) -> None:
    super().__init__(model_name, provider, max_tokens, temperature, pricing_plan)
    self.api_key= api_key

  def generate_response(self, prompt: str) -> str:
    self.validate_prompt(prompt)
    self.log(f'Sending request to {self.model_name}')
    return self._build_response('GPT API', prompt)

  
class LlamaModel(LanguageModel,):
  def __init__(self, model_name: str, provider: str, max_tokens: int,
              temperature: float,model_path: str, quantization: str,
              pricing_plan: PricingPlan) -> None:
    super().__init__(model_name, provider, max_tokens, temperature, pricing_plan)
    self.model_path= model_path
    self.quantization= quantization

  def generate_response(self, prompt):
    return self._build_response('Local Llama', prompt)