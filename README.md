Connect 4
=========
[![Coverage Status](https://coveralls.io/repos/github/palfrey/connect4/badge.svg)](https://coveralls.io/github/palfrey/connect4)

Command line version of [Connect 4](https://en.wikipedia.org/wiki/Connect_Four).

Usage
-----
1. Install Python 3.x. Tested on 3.7-3.11.
2. Run `python connect4.py`. Optionally, provide it some arguments for a non-default game.
```
  --players PLAYERS     Players (default: 2)
  --rows ROWS           Rows in the grid (default: 6)
  --columns COLUMNS     Columns in the grid (default: 7)
  --winning-count WINNING_COUNT
                        Winning number of counters in a row (default: 4)
````

Development
-----------
1. Install the testing/dev packages with `pip install -r requirements.txt`
    * Optionally (but encouraged), setup a [virtualenv](https://docs.python.org/3/library/venv.html#creating-virtual-environments) first!
2. Setup [pre-commit](https://pre-commit.com/) with `pre-commit install`

[pytest-watch](https://pypi.org/project/pytest-watch/) is installed for watching tests, and a suggested command line for running tests is `ptw -- -vvv --cov=. --cov-report=term-missing`

If you add new packages to the `requirements.in`, please re-run `pip-compile` to generate the locked-down version in `requirements.txt`.
