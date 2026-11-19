"""Tests for the whole project."""
from conversation import Conversation
from exceptions import InvalidPromptError
from manager import ModelManager
from models import GPTModel, LanguageModel, LlamaModel
from pricing import PricingPlan
from tokenizer import Tokenizer



def build_manager() -> ModelManager:
    """Create the pricing plan, both models, and a manager holding them."""
    pricing = PricingPlan("Standard", 0.02)
    manager = ModelManager()
    manager.add_model(GPTModel("GPT-Model", "OpenAI", 4096, 0.7, "secret-key", pricing))
    manager.add_model(LlamaModel("Llama-Model", "Local", 8192, 0.5,
                                 "/models/llama", "4-bit", pricing))
    return manager


def main() -> None:
    # 1. Object creation
    pricing = PricingPlan("Standard", 0.02)
    gpt = GPTModel("GPT-Model", "OpenAI", 4096, 0.7, "secret-key", pricing)
    llama = LlamaModel("Llama-Model", "Local", 8192, 0.5,
                       "/models/llama", "4-bit", pricing)
    manager = ModelManager()
    manager.add_model(gpt)
    manager.add_model(llama)

    # 2. Info, class/static methods, magic methods
    print(gpt, repr(gpt), len(gpt))
    gpt.display_info()
    print(LanguageModel.get_total_models())
    print(LanguageModel.validate_temperature(0.7), LanguageModel.validate_temperature(3.5))
    print(gpt == GPTModel("GPT-Model", "OpenAI", 1, 0.1, "k", pricing))
    print(Tokenizer().count_tokens("Artificial intelligence is powerful"))

    # 3. Abstraction
    try:
        LanguageModel("x", "y", 1, 0.5, pricing)  # type: ignore[abstract]
    except TypeError as error:
        print(f"Abstract: {error}")

    # 4. Polymorphism
    for model in (gpt, llama):
        print(model.generate_response("Explain OOP"))

    # 5. Encapsulation
    gpt.temperature = 1.2
    print(gpt.temperature)
    try:
        gpt.temperature = 4
    except ValueError as error:
        print(error)

    # 6. Exceptions
    for bad in ("", "   ", 123):
        try:
            gpt.generate_response(bad)  # type: ignore[arg-type]
        except InvalidPromptError as error:
            print(f"Error: {error}")

    # 7. Conversation
    conversation = Conversation(1, gpt)
    conversation.send_message("Explain object-oriented programming")
    conversation.display_history()

    # 8. Cost
    gpt.calculate_request_cost("Explain machine learning")

    # 9. Manager selection
    print(manager.select_model("Local", 5000))
    llama.is_active = False
    print(manager.select_model("Local", 5000))


if __name__ == "__main__":
    main()
