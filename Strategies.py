from abc import ABC, abstractmethod
from collections import deque

try:
    from data_loader import MarketDataPoint
except ModuleNotFoundError as e:
    print(f"Fatal! Source Broken. Please implement module 'data_loader'. Error! {e}. ")

class Strategy(ABC):
    @abstractmethod
    def generate_signals(self, tick: MarketDataPoint) -> list:
        pass

class MAC(Strategy):
    def __init__(self,short_window:int=5,long_window:int=20):
        self._short_window = short_window
        self._long_window = long_window
        self._short_prices = deque(maxlen=short_window)
        self._long_prices = deque(maxlen=long_window)
        self._last_signal = None

    def generate_signals(self, tick: MarketDataPoint) -> list:
        """Return a list of signals"""
        self._short_prices.append(tick.price)
        self._long_prices.append(tick.price)
        #sanity check
        if len(self._short_prices)<self._short_window or len(self._long_prices)<self._long_window:
            return []
        #\frac{1}{n} \sum {price_{i}}
        signals = []
        short_ma = sum(self._short_prices)/len(self._short_prices)
        long_ma = sum(self._long_prices)/len(self._long_prices)
        if short_ma>long_ma and self._last_signal!="BUY":
            signals.append("BUY")
            self._last_signal = "BUY"
        if short_ma<long_ma and self._last_signal!="SELL":
            signals.append("SELL")
            self._last_signal="SELL"
        return signals

class Momentum(Strategy):
    """exposure reduced momentum strategy"""
    def __init__(self,window:int = 10):
        self._window = window
        self._prices = deque(maxlen= window)
        self._last_signal = None
    def generate_signals(self, tick: MarketDataPoint) -> list:
        """Return a list of signals"""
        self._prices.append(tick.price)
        if len(self._prices) < self._window:
            return []
        momentum =tick.price - self._prices[0]
        signals = []
        if momentum>0 and self._last_signal!="BUY":
            signals.append("BUY")
            self._last_signal = "BUY"
        if momentum<0 and self._last_signal!="SELL":
            signals.append("SELL")
            self._last_signal="SELL"
        return signals
