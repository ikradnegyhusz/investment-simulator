# Investing Simulation
Simulate decades of stock market investing in minutes
## Structure
- "simulator.py" is the main file for the simulation
- "webscrape.py" downloads real stock market data into "chart_data" folder based on tickers in "bats_symbols.csv"
- "clear_junk.py" script removes small files from "chart_data" folder
- "scores.txt" contains information about the investor's performance (see source code for details)

## How it works
"simulator.py" displays chart data of a random stock. The user has a fixed starting balance, and can skip days (either 1 or 15) and choose when to buy or sell. Once the days are finished a new chart is randomized and the player's balance is reset. Final balance is saved automatically.

## Controls
- move chart horizontally: left mouse button + drag
- move chart vertically: right mouse button + drag
- zoom: mouse wheel
- progress day: d
- progress 15 days: f
- stretch chart horizontally: arrow up, arrow down
- buy (with all current money): b
- select amount to invest: numpad, enter, backspace
- sell: s
- new chart: n
- scroll automatically to end: space
- fullscreen: F11