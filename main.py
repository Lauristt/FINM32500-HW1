try:
    from data_loader import MarketDataPoint, read_market_data_fixed
    from engine import ExecutionEngine
    from Strategies import MAC, Momentum
    from reporting import PerformanceReporter
except ModuleNotFoundError as e:
    print(f"Fatal! A required module is missing. Please ensure all .py files are in the same directory. Error: {e}.")


def main(csv_filename, strategy, initial_cash=100000):
    print(f"Loading market data from '{csv_filename}'...")
    ticks = read_market_data_fixed(csv_filename)
    if not ticks:
        print("Could not load market data. Aborting...")
        return

    print(f"Loaded {len(ticks)} data points.")
    print("Initializing strategy...")

    if strategy == 'MAC':
        try:
            mac_strategy = MAC(short_window=10, long_window=30)
            print("Initializing backtesting engine...")
            engine = ExecutionEngine(strategies=[mac_strategy], initial_cash=initial_cash)
        except Exception as e:
            print(f"Error initializing MAC strategy: {e}")
            raise
    elif strategy == 'Momentum':
        try:
            momentum_strategy = Momentum(window=10)
            print("Initializing backtesting engine...")
            engine = ExecutionEngine(strategies=[momentum_strategy], initial_cash=initial_cash)
        except Exception as e:
            print(f"Error initializing Momentum strategy: {e}")
            raise
    else:
        print(f"Strategy '{strategy}' not recognized. Aborting...")
        raise ValueError(f"Unknown strategy: {strategy}")

    print("Running backtest...")
    results = engine.run(ticks)
    print("Backtest completed.")

    if results and results.get("equity_curve"):
        print("Generating performance report...")
        reporter = PerformanceReporter(results)
        reporter.generate_report(filename="performance_report.md")
    else:
        print("No results were generated, skipping report.")

if __name__ == "__main__":
    filepath = '/Users/laurisli/Desktop/FINM32500/HW1/market_data.csv'
    ## Strategy can be 'Momentum' or 'MAC'.
    main(filepath,"MAC")