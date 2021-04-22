# Actions
Actions are JSON-like dictionaries used to send user interactions to our backend. Users won't ever really see this, but whatever they do will be sent as a dictionary with the primary keys of "action" and "gameState". "action" is a string used to label what logic should be used, and what other keys are expected. "gameState" is used to keep track of who's turn it is.

## Possible Actions, and what keys to send and why
### "attack"
Attacks require the following keys:
- "target", for picking out what entity to deal damage to.
- "value", for defining how much damage to deal to said entity.
- "cur_value", for remembering the target's current health
### "draw"
Drawing a card(s) needs the following keys:
- "actor", who is drawing the card
- "value", how many cards will be drawn