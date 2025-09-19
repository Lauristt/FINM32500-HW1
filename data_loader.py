import csv
import dataclasses
from datetime import datetime
from typing import List
@dataclasses.dataclass(frozen=True)
class MarketDataPoint:
    timestamp: datetime
    symbol: str
    price: float


def read_market_data_fixed(filename: str) -> List[MarketDataPoint]:
    data_points = []
    try:
        with open(filename, 'r', newline='') as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip header
            for row in reader:
                try:
                    timestamp = datetime.fromisoformat(row[0])
                    symbol = row[1]
                    price = float(row[2])
                    data_points.append(MarketDataPoint(timestamp, symbol, price))
                except (ValueError, IndexError) as e:
                    print(f"Skipping row due to parsing error: {row}. Error: {e}")
    except FileNotFoundError:
        print(f"Error: The data file '{filename}' was not found.")
        print("Please run 'data_generator.py' first to create it.")
    return data_points

