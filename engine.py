import random
from typing import List, Dict, Tuple
import logging

try:
    from models import Order, OrderError, ExecutionError, OrderStatus
    from data_loader import MarketDataPoint
    from Strategies import Strategy, MAC, Momentum
except ModuleNotFoundError as e:
    print(f"Fatal! Source Broken. Please implement module 'models' or  'data_loader' or 'Strategies'. Error! {e}. ")

logger = logging.getLogger("backtest")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(handler)

class ExecutionEngine:
    def __init__(self,strategies: List[Strategy], initial_cash: float = 100000.0, default_quantity: int = 10):
        self.strategies = strategies
        self.cash = initial_cash
        self.portfolio : Dict[str,Dict[str,float]] = {}
        self.equity_curve : List[Tuple] = []
        self.default_quantity = default_quantity

    def _create_order_from_signal(self,sig:Tuple[str,str,int,float]) -> Order:
        direction, symbol, quantity, price = sig
        # some sanity checks
        if direction not in ("BUY", "SELL"):
            raise OrderError("Can not identify trade direction. Dataset is corrupted. Aborting...")
        if quantity<=0:
            raise OrderError("Quantity must be strictly positive. Aborting..")
        order =Order(symbol= symbol, quantity = quantity, price = price,side = direction)
        return order

    def _simulate_execution(self,order:Order) -> None:
        # Core Trading Logic, allows turnover and short positions
        # order: symbol, quantity, price, direction
        # implement HW Requirement: In the execution engine, simulate occasional failures and raise ExecutionError; catch and log these errors to continue processing.
        if random.random() < 0.02:  # 2% chance to fail
            raise ExecutionError("Simulated execution failure")
        symbol= order.symbol
        pos = self.portfolio.get(symbol, {"quantity": 0.0, "avg_price": 0.0})
        current_qty = pos["quantity"]
        current_avg_price = pos["avg_price"]

        order_qty = order.quantity
        order_price = order.price

        if order.side == "BUY":
            self.cash -= order_qty * order_price
            new_qty = current_qty + order_qty

            if current_qty < 0 and new_qty > 0:
                pos["avg_price"] = order_price
            elif new_qty > 0:
                new_total_cost = (current_avg_price * current_qty) + (order_price * order_qty)
                pos["avg_price"] = new_total_cost / new_qty
            else:
                pos["avg_price"] = current_avg_price if new_qty < 0 else 0.0

            pos["quantity"] = new_qty

        else:  # order.side == "SELL"
            self.cash += order_qty * order_price
            new_qty = current_qty - order_qty

            if current_qty > 0 and new_qty < 0:
                pos["avg_price"] = order_price
            elif new_qty < 0:
                new_total_value = (current_avg_price * abs(current_qty)) + (order_price * order_qty)
                pos["avg_price"] = new_total_value / abs(new_qty)
            else:
                pos["avg_price"] = current_avg_price if new_qty > 0 else 0.0

            pos["quantity"] = new_qty

        self.portfolio[symbol] = pos
        order.mark_filled()

    def _compute_equity(self, tick: MarketDataPoint) -> float:
        # compute holdings marked to market using tick price if symbol exists
        # (logics can be optimized if we have several stocks)

        total = self.cash
        for sym, pos in self.portfolio.items():
            # symbol,{"quantity":0.0,"avg_price":0.0}
            # if current tick symbol matches, use tick.price; else use pos['avg_price'] as proxy
            p = tick.price if sym == tick.symbol else pos.get("avg_price", 0.0)
            total += pos["quantity"] * p
        return total

    def run(self, ticks: List[MarketDataPoint]):
        for tick in ticks:
            all_signals = []
            for strat in self.strategies:
                try:
                    signals = strat.generate_signals(tick)
                    if signals:
                        all_signals.extend(signals)
                except Exception as e:
                    logger.exception(f"Error encountered when executing Strategy: {strat}.  Error: {e}")

            for direction in all_signals:
                order = None
                try:
                    signal_tuple = (direction, tick.symbol, self.default_quantity, tick.price)
                    order = self._create_order_from_signal(signal_tuple)
                    order.status = OrderStatus.PENDING
                    order.validate()
                    self._simulate_execution(order)
                except OrderError as oe:
                    logger.error(f"Signal {direction} Encountered Error: {oe}")
                except ExecutionError as ee:
                    if order:
                        order.mark_failed(reason=str(ee))
                    logger.error(f"Order {order} Encountered ExecutionError: {ee}")
                except Exception as e:
                    if order:
                        order.mark_failed(reason=str(e))
                    logger.exception(f"Unknown Error when dealing with signal: {direction}. Error: {e}")

            equity = self._compute_equity(tick)
            self.equity_curve.append((tick.timestamp, equity))

        return {
            "final_cash": self.cash,
            "portfolio": self.portfolio,
            "equity_curve": self.equity_curve
        }

