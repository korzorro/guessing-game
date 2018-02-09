# guessing-game
A guessing game api for chat bots

## Description
This game is designed to let users guess and let users see the closest guess(es) to a number. Ties are allowed. For every new game, a user may guess only once. As soon as someone does not want there to be more guessing, guessing can be disabled. It can also be reenabled. When the results are in, the winner(s) will be revealed.

## Usage
The game api is hosted on guessing-game.korzon.ninja
### Tokens
You need to have a token to play a game. You can acquire one at `guessing-game.korzon.ninja/generate-token` Keep this token secret. When you integrate it into your bot, make sure the token is in each command in the query string. 
### New Game
To start a new game visit `guessing-game.korzon.ninja/new-game?token={token}` This will enable guessing and clear all guesses.
### Guessing
To submit a guess visit `guessing-game.korzon.ninja/guess?token={token}&guess={guess}&user={user}` Note that the username must be given when making a guess. A guess can only be of integer value.
### Results
To find out the winner(s) of the game, visit `guessing-game.korzon.ninja/results?token={token}&answer={answer}` Each winner will be listed, but the game will not reset. You can sent the requeste again with a different answer any time to check the results if the answer was different.
### Enable/Disable Guessing
To disallow guessing go to `guessing-game.korzon.ninja/disable-guessing?token={token}` This is used to close guessing to general users in the case that there is an outcome approaching where guessing to close to that outcome would give new guessers an unfair advantage. You can reenable guessing at `guessing-game.korzon.ninja/enable-guessing?token={token}`

## Example
First make sure to generate your token to place in the url section of these commands. Generate a token at guessing-`game.korzon.ninja/generate-token` That token will now replace `{token}` in each of these examples. 
### Nightbot
Nightbot is a common chat bot made popular by those on twitch.tv. You can learn about all of it's functionality at beta.nightbot.tv. The following is a guide for the commands you can add to your channel's nightbot to be able to play this game.


`!guess $(urlfetch https://guessing-game.korzon.ninja/guess?token={token}user=$(user)&guess=$(1))`

`!newgame $(urlfetch https://guessing-game.korzon.ninja/new-game?token={token})`

`!disableguessing $(urlfetch https://guessing-game.korzon.ninja/disable-guessing?token={token})`

`!enableguessing $(urlfetch https://guessing-game.korzon.ninja/enable-guessing?token={token})`

`!results $(urlfetch https://guessing-game.korzon.ninja/results?token={token})`


After adding those five commands to your twitch channel's nightbot. You should be all set to play. The command name is to the left and the `$(urlfetch...` section is what you want to set your command to do. So you can add a command like this.


`!commands add !guess $(urlfetch https://guessing-game.korzon.ninja/guess?token={token}user=$(user)&guess=$(1))`


To guess, type `!guess {number}`

To start a new game type `!newgame`

To disable guessing type `!disableguessing`

To enable guessing type `!enableguessing`

To view the results type `!results`
