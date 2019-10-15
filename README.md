# Dominion Simple AI
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


Example of output:
```

python dominion_simple_ai.py                                                                                                                                            ▸▸▸▸▸▸▸▹▹▹
Starting a new game

    Turns so far: 0
    Victory points so far: 3
    All cards: Counter({'copper': 7, 'estate': 3})
        Hand: Counter({'copper': 4, 'estate': 1})
        Discard: Counter()
        Deck: Counter({'copper': 3, 'estate': 2})

Press Enter to take a turn...

    Turns so far: 0
    Victory points so far: 3
    All cards: Counter({'copper': 7, 'estate': 3})
        Hand: Counter({'copper': 4, 'estate': 1})
        Discard: Counter()
        Deck: Counter({'copper': 3, 'estate': 2})
Hand has buying power 4...
(Speaking: I have 4 copper and 1 estate)
(Speaking: for total buying power of 4)
(Speaking: I buy silver)

Press Enter to take a turn...

    Turns so far: 1
    Victory points so far: 3
    All cards: Counter({'copper': 7, 'estate': 3, 'silver': 1})
        Hand: Counter({'copper': 3, 'estate': 2})
        Discard: Counter({'copper': 4, 'silver': 1, 'estate': 1})
        Deck: Counter()
Hand has buying power 3...
(Speaking: I have 3 copper and 2 estate)
(Speaking: for total buying power of 3)
(Speaking: I buy silver)

Press Enter to take a turn...

    Turns so far: 2
    Victory points so far: 3
    All cards: Counter({'copper': 7, 'estate': 3, 'silver': 2})
        Hand: Counter({'copper': 4, 'silver': 1})
        Discard: Counter()
        Deck: Counter({'estate': 3, 'copper': 3, 'silver': 1})
Hand has buying power 6...
(Speaking: I have 4 copper and 1 silver)
(Speaking: for total buying power of 6)
(Speaking: I buy gold)

Press Enter to take a turn...



```
