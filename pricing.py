class PricingPlan:
  def __init__(self, plan_name: str, price_per_1000_tokens: float) -> None:
    self.plan_name= plan_name
    self.price_per_1000_tokens= price_per_1000_tokens

  def calculate_cost(self, tokens: int) -> float:
      """Return the cost of `tokens` under this plan."""
      return tokens / 1000 * self.price_per_1000_tokens
