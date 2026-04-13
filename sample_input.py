class OrderService:
    def create_order(self, customer_id: int, amount: float) -> dict:
        if customer_id <= 0:
            raise ValueError("customer_id must be positive")

        if amount <= 0:
            raise ValueError("amount must be positive")

        fee = amount * 0.05
        total = amount + fee

        return {
            "customer_id": customer_id,
            "amount": amount,
            "fee": fee,
            "total": total,
            "status": "created",
        }
