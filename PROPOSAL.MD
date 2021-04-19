# Final Turn, the Card Game

## Description and Motivation
Final Turn will be an online card game where users compete their cards against other players. The game will feature
deck customization, 2-player games, tracking of W/L ratios, and some basic visuals. We wanted to show off our skills with Channels and Websockets by creating a browser-based turn based game.

## Prior Art
Yu-Gi-Oh is definitely the biggest inspiration for this card game. Many of the core concepts apply here, although there are core differences, like how our cards have hit points, rather than being destroyed in one hit.

## Core User Workflows
By the end of the week, users will be able to do the following:
- Sign up, Login, and Logout.
- Send, Accept, and Unfriend other people .
- Leaderboards.
- Connect to and create game lobbies (Home page will show open game lobbies).
- Battle with other players (win state when 1 player runs out of Life Points).
  - Each turn will have 2 major phases: Main Phase and Battle Phase.
  - During a player's Main Phase, they can place up to 1 Monster Card and play as a many Effect (Spell) Cards as they wish from their hand. Used Effect Cards are sent to the Discard Pile once their effect concludes.
  - During a player's Battle Phase, they can declare attacks with any available monsters on their side of the field. Monsters hit by an attack lose HP based on their attacker's ATK stat minus their own defense. Cards with zero HP are sent to the Discard Pile.

## Daily Goals

### Monday
Both Matt and Travis will collaberate on setting up the project itself, installing all the dependencies, and making sure we can boot the site locally. If we have time, we can implement user signup, login, and logout.

### Tuesday
Matt will work on establishing the websocket system, allowing users to connect to each other in "Lobbies", and start on game logic. Travis will work on the Cards model/some game logic. Both of us will be communicating on our work here on the game's rules and actual JavaScript to run it.

### Wednesday
Matt will work completing the main game loop (allowing users to battle until a win/lose state is achieved), and record that to the user. Travis will work on Deck Customization, and possibly adding a way for users to get new cards.

### Thursday
Both Matt and Travis will work on deploying the app and populating the Heroku database with the actual cards we compiled together. If there is any time left that day, we will focus on testing and adding any new cards.

### Friday
If everything goes right, this day will be testing and adding quality of life things (theme customization, vanity fields, vanity cards, extra card effects)
