class Tokenizer:
    """Counts tokens, where every word is one token."""
    def count_tokens(self, text: str) -> int:
        return len(text.split())

