# LLM Management System

A Python project that manages simulated language models (GPT and Llama) and applies 19 object-oriented programming concepts in one working system. It includes a test script and a Streamlit app with a model sidebar and chat.

No real API is called. Every response is simulated.

## Features

- Abstract base class `LanguageModel` with two child models, `GPTModel` and `LlamaModel`
- Prompt validation with a custom exception, `InvalidPromptError`
- Temperature and model status protected behind properties
- Word-based token counting and request cost calculation from a pricing plan
- `ModelManager` to store models and select one by provider, token limit and status
- `Conversation` to keep message history for a model
- Streamlit app with a model sidebar, chat, and a model info tab

## Project structure

```
llm_oop_project/
├── models.py          LanguageModel, GPTModel, LlamaModel, LoggingMixin
├── tokenizer.py       Tokenizer
├── pricing.py         PricingPlan
├── conversation.py    Conversation
├── manager.py         ModelManager
├── exceptions.py      InvalidPromptError
├── main.py            Tests for all classes
├── app.py             Streamlit app
└── .streamlit/
    └── config.toml    App theme
```

## OOP concepts and where they appear

| Concept | Where |
|---|---|
| Abstraction | `LanguageModel` inherits `ABC`, and `generate_response()` is abstract |
| Inheritance and overriding | `GPTModel` and `LlamaModel` override `generate_response()` |
| Polymorphism | `main.py` calls `generate_response()` on every model in a loop |
| Multiple inheritance | `GPTModel` inherits `LanguageModel` and `LoggingMixin` |
| Encapsulation and properties | Private `__temperature` and `__is_active` with getters and setters |
| Class attribute and class method | `total_models` and `get_total_models()` |
| Static method | `validate_temperature()` |
| Composition | Each model creates its own `Tokenizer` |
| Aggregation | A `PricingPlan` is passed into each model and outlives it |
| Magic methods | `__str__`, `__repr__`, `__len__`, `__eq__`, `__hash__` |
| Custom exception | `InvalidPromptError` for empty, blank or non-string prompts |

## Requirements

- Python 3.10 or newer
- Streamlit, only for the app

```
pip install streamlit
```

## Usage

Run the test script from the project folder:

```
python main.py
```

It covers object creation, model execution, polymorphism, encapsulation, exception handling, a conversation and a request cost calculation.

Run the app:

```
streamlit run app.py
```

Run both commands from the project root, so Python can find the modules and Streamlit can find `.streamlit/config.toml`. Restart Streamlit after changing the theme file.

## Example

```python
from main import build_manager
from conversation import Conversation

manager = build_manager()
gpt = manager.get_model("GPT-Model")

chat = Conversation(1, gpt)
chat.send_message("Explain object-oriented programming")
chat.display_history()

gpt.calculate_request_cost("Explain machine learning")
# Input tokens: 3
# Request cost: $0.000060
```

Cost is calculated as `tokens / 1000 * price_per_1000_tokens`, and one word counts as one token.

## Model selection

```python
manager.select_model("Local", 5000)   # returns Llama-Model
```

`select_model()` returns the first model that matches the provider, has `max_tokens` at least equal to the requested amount, and is active. If none fits, it returns `None`.

## Connecting a real API

Only `generate_response()` needs to change. Replace the simulated text in `GPTModel` or `LlamaModel` with a call to the real service, and keep prompt validation, token counting, cost calculation and conversation history as they are.
