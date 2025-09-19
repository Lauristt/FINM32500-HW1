import enum
from typing import Optional
from dataclasses import dataclass

try:
    from data_loader import MarketDataPoint
except ModuleNotFoundError as e:
    print(f"Fatal! Source Broken. Please implement module 'data_loader'. Error! {e}. ")

class OrderStatus(enum.Enum):
    NEW = "NEW"
    PENDING = "PENDING"
    FILLED = "FILLED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"

@dataclass
class Order:
    symbol: str
    quantity: int
    price: float
    status: OrderStatus = OrderStatus.NEW
    side: str = "BUY"  # or "SELL"
    filled_quantity: int = 0

    def validate(self):
        if self.quantity == 0:
            raise OrderError("Order quantity cannot be zero")
        if abs(self.quantity) < 0:
            raise OrderError("Order quantity cannot be negative")

    def mark_filled(self, filled_qty: Optional[int] = None):
        filled_qty = filled_qty if filled_qty is not None else self.quantity
        self.filled_quantity = filled_qty
        self.status = OrderStatus.FILLED

    def mark_failed(self, reason:str=""):
        self.status = OrderStatus.FAILED

    def mark_rejected(self, reason:str=""):
        self.status = OrderStatus.REJECTED


class OrderError(Exception):
    """Raised when an invalid order is created."""
    pass

class ExecutionError(Exception):
    """implement HW Requirement: In the execution engine, simulate occasional failures and raise ExecutionError; catch and log these errors to continue processing."""
    pass


if __name__ == "__main__":
    unit_test_order = Order("AAPL", 100, 1000, "long")
    # timestamp, symbol, price
    unit_test_mdp = MarketDataPoint("2025-09-19 00:45:12","AAPL",1000)
    try:
        unit_test_mdp.price = 1000
    except Exception as e:
        print(f"Overwrite attr error! Error: {e}")


