# dominion_simple_ai
A very simple ai/bot for Dominion

This is a simple ai/bot for the card game Dominion.  It simply plays a "greens
and golds" strategy, buying the most expensive money cards possible, or a
province.  In late game (>3 provinces already gained), it simply buys the most
expensive victory point cards.


## How to use

- Download this repo (or just the `dominion_simple_ai.py` file)
- Open Terminal, and `cd` to the directory with `dominion_simple_ai.py`
- Run `python dominion_simple_ai.py`

This is designed to run on macOS (if you don't like that, you can modify the
speak_str() function to not use the macOS `say` command for Text to Speech),
and Python 3 (if you don't like that, please consider updating).
