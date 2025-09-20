<p align="center"><h1 align="center">FINM32500-HW1</h1></p>
<p align="center"><h3 align="center">Author: Yuting Li, Rajdeep Choudhury, Xiangchen Liu, Dylan Pan</h3></p>
<p align="center"><!-- default option, no dependency badges. -->
</p>
<p align="center">
    <!-- default option, no dependency badges. -->
</p>


##  Overview

This project is a modular, event-driven backtesting framework written in Python. It is designed to simulate trading strategies against historical or generated market data to evaluate their performance. The framework is built with a clear separation of concerns, making it easy to introduce new strategies, data sources, or performance metrics. At its core, it provides a simulation engine that processes market ticks, executes trades based on strategy signals, and tracks the portfolio's equity over time.

##  Features
1. Event-Driven Architecture: The core engine processes market data tick-by-tick, simulating a live trading environment.
2. Modular Design: Components for data handling, strategy logic, execution, and reporting are separated, allowing for easy modification and extension.
3. Extensible Strategy Interface: Includes a base Strategy class and two sample implementations: Moving Average Crossover (MAC) and Momentum.
4. Data Simulation: A data generator is included to create realistic, customizable market data using a Gaussian random walk.
5. Realistic Trade Execution: The engine simulates order processing and includes a configurable failure rate to mimic real-world execution uncertainty.
6. Performance Analytics: Automatically calculates key metrics like Total Return, Sharpe Ratio (per-tick), and Maximum Drawdown.
7. Automated Reporting: Generates a clean, readable performance summary in a Markdown file (performance_report.md), complete with an ASCII art equity curve.

##  Project Structure


```sh
└── FINM32500-HW1/
    ├── Strategies.py
    ├── data_generator.py
    ├── data_loader.py
    ├── engine.py
    ├── main.py
    ├── market_data.csv
    ├── models.py
    ├── performance_report.md
    └── reporting.py
```
###  Project Index

<details open>
    <summary><b><code>FINM32500-HW1/</code></b></summary>
    <details> <!-- root Submodule -->
        <summary><b>root</b></summary>
        <blockquote>
            <table>
            <tr>
                <td><b><a href='https://github.com/Lauristt/FINM32500-HW1/blob/master/data_generator.py'>data_generator.py</a></b></td>
                <td>Generates simulated time-series market data and saves it to a CSV file.</td>
            </tr>
            <tr>
                <td><b><a href='https://github.com/Lauristt/FINM32500-HW1/blob/master/main.py'>main.py</a></b></td>
                <td>The main entry point to run the entire backtesting simulation.</td>
            </tr>
            <tr>
                <td><b><a href='https://github.com/Lauristt/FINM32500-HW1/blob/master/reporting.py'>reporting.py</a></b></td>
                <td>Calculates performance metrics from backtest results and generates the final report.</td>
            </tr>
            <tr>
                <td><b><a href='https://github.com/Lauristt/FINM32500-HW1/blob/master/engine.py'>engine.py</a></b></td>
                <td>Contains the core backtesting engine that processes data and simulates trades.</td>
            </tr>
            <tr>
                <td><b><a href='https://github.com/Lauristt/FINM32500-HW1/blob/master/data_loader.py'>data_loader.py</a></b></td>
                <td>Reads and parses market data from a CSV file into data objects.</td>
            </tr>
            <tr>
                <td><b><a href='https://github.com/Lauristt/FINM32500-HW1/blob/master/Strategies.py'>Strategies.py</a></b></td>
                <td>Defines the abstract base class for strategies and includes sample implementations (MAC, Momentum).</td>
            </tr>
            <tr>
                <td><b><a href='https://github.com/Lauristt/FINM32500-HW1/blob/master/models.py'>models.py</a></b></td>
                <td>Defines core data structures like Order, OrderStatus, and custom exceptions.</td>
            </tr>
            </table>
        </blockquote>
    </details>
</details>

##  Getting Started

###  Prerequisites

Before getting started with FINM32500-HW1, ensure your runtime environment meets the following requirements:

    Programming Language: Python 3.x (No external libraries are required).

###  Installation (Build from source)

Clone the FINM32500-HW1 repository:

	git clone [https://github.com/Lauristt/FINM32500-HW1](https://github.com/Lauristt/FINM32500-HW1)

Navigate to the project directory:

	cd FINM32500-HW1

No further installation is needed as the project only uses standard Python libraries.

###  Usage
To run the simulation on Linux Server, follow these steps:

Generate Market Data:First, run the data generator script to create the market_data.csv file.

    python data_generator.py

Run the Backtest: Execute the main script to run the backtest with the chosen strategy (configurable in main.py).

    python main.py

View Results: After the simulation finishes, a performance_report.md file will be created in the project directory. Open this file to view the results.

##  Project Roadmap

[X] Core Framework: <strike>Implement the modular, event-driven backtesting engine.</strike>

[X] Basic Strategies: <strike>Implement Moving Average Crossover and Momentum strategies.</strike>

[X] Performance Reporting: <strike>Implement reporting with key metrics and ASCII equity curve.</strike>

##  Contributing

💬 Join the Discussions: Share your insights, provide feedback, or ask questions.

🐛 Report Issues: Submit bugs found or log feature requests for the FINM32500-HW1 project.

💡 Submit Pull Requests: Review open PRs, and submit your own PRs.

<details closed>
	

<summary>Contributor Graph</summary>
<br>
<p align="left">
   <a href="https://github.com{/Lauristt/FINM32500-HW1/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=Lauristt/FINM32500-HW1">
   </a>
</p>
</details>

##  License

This project is protected under the MIT LICENSE. For more details, refer to the LICENSE file.

##  Acknowledgments

This project was created as part of the FINM 32500 course at The University of Chicago. Inspiration from various open-source backtesting frameworks.
