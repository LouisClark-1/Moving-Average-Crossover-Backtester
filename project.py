import numpy as np
import yfinance as yf
import argparse
import sys
import seaborn as sns
import matplotlib.pyplot as plt


def main():
    sns.set_theme()
    chosen_ticker = get_ticker()
    datas = get_data(chosen_ticker)
    yhold, hold_return = buy_and_hold(datas)
    ybin, bin_return = binary_strategy(*get_averages_and_returns(datas))
    yvar, var_return = variable_strategy(*get_averages_and_returns(datas))
    days = yhold.size
    plt.plot(np.arange(0, days), yhold, color="blue", label="Hold")
    plt.plot(np.arange(0, days), ybin, color="red", label="Binary")
    plt.plot(np.arange(0, days), yvar, color="green", label="Variable")
    plt.title(chosen_ticker)
    plt.legend()
    print(f"Holding saw {(hold_return*100):.1f}% change, "
          f"the binary strategy saw a {(bin_return*100):.1f}% change, "
          f"and the variable strategy saw a {(var_return*100):.1f}% change."
          f"({chosen_ticker})"
    )
    plt.show()


def get_ticker(test_args=None):
    parser = argparse.ArgumentParser(description="This program backtests your chosen stock based on two strategies")
    parser.add_argument("-t", "--ticker", type=str, default=None, help="Your chosen ticker")
    args = parser.parse_args(test_args)   # this allows us to test this function. since test_args is None by default, parse_args just uses the actual argv until we input one for the test
    if not args.ticker:
        sys.exit("No ticker entered")
    return args.ticker


def get_data(user_ticker):
    ticker = yf.Ticker(user_ticker)
    data = ticker.history(period="1y", interval="1d")
    if data["Close"].size < 20:
        sys.exit("Insufficient data")
    return data["Close"].to_numpy()


def get_averages_and_returns(prices: np.ndarray): # returns 20 day moving avg, 5 day moving avg, decimal change in price that day leading to the close price
    return (np.convolve(prices, np.ones(20)/20, mode='valid'), np.convolve(prices[15:], np.ones(5)/5, mode='valid'),
        (prices[19:] / prices[18:-1]) - 1)
        

def buy_and_hold(prices):  # buys $1000 on day 20 and holds
    prices = prices[19:]
    noShares = 1000 / prices[0]
    investment = prices * noShares
    return investment, (investment[-1] - 1000) /1000


def binary_strategy(avg20, avg5, returns):
    actions = avg5 >= avg20
    returns = np.roll(returns, shift=-1) # this ensures we get the next day's result after chosing to buy at the end of the day
    dailymove = np.where(actions, returns, 0)
    dailymove = np.concatenate(([0], dailymove[:-1])) # this makes our first waiting day a 0, and removes the last element which was actually the first waiting day element but we rolled it over
    return np.cumprod(dailymove + 1) * 1000, np.prod(dailymove + 1) - 1

def variable_strategy(avg20, avg5, returns):
    change_in_avg = (avg5 / avg20) - 1
    returns = np.roll(returns, shift=-1)
    conditions = [
        change_in_avg < -0.005,
        change_in_avg < 0.005,
        change_in_avg < 0.015,
        change_in_avg < 0.025,
    ]
    proportion_invested = np.select(conditions, [0, 0.25, 0.5, 0.75], default=1)
    # ^ np.select takes the first one that satisfies the condition
    multipliers = (returns * proportion_invested) + 1
    multipliers = np.concatenate(([1], multipliers[:-1]))
    return np.cumprod(multipliers) * 1000, np.prod(multipliers) - 1

if __name__ == "__main__":
    main()