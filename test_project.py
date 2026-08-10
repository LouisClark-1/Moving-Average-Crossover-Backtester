import pytest
import numpy as np
from project import get_averages_and_returns, buy_and_hold, get_ticker


def test_get_ticker():
    assert get_ticker(["-t", "MSFT"]) == "MSFT"
    assert get_ticker(["--ticker", "AAPL"]) == "AAPL"
    with pytest.raises(SystemExit):
        get_ticker([""])

def test_buy_and_hold():
    assert buy_and_hold(np.ones(22))[0].tolist() == [1000, 1000, 1000]
    assert buy_and_hold(np.ones(22))[1] == 0
    assert buy_and_hold(np.concatenate((np.ones(20), [2, 3, 4])))[0].tolist() == [1000, 2000, 3000, 4000]
    assert buy_and_hold(np.concatenate((np.ones(20), [2, 3, 4])))[1] == 3

def test_get_averages_and_returns():
    assert get_averages_and_returns(np.ones(22))[0].tolist() == [1, 1, 1]
    assert get_averages_and_returns(np.ones(22))[1].tolist() == [1, 1, 1]
    assert get_averages_and_returns(np.ones(22))[2].tolist() == [0, 0, 0]
    