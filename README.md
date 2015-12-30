# tweet-tac-toe

This is a Twitter bot that plays Tic-Tac-Toe with other users on Twitter. The bot parses the
ASCII representation of the board in tweets that mention [@TweetTacToeBot](https://twitter.com/TweetTacToeBot) and uses a minimax
search algorithm to find the optimal move based on the state that the game is currently in.
It is connected to a MongoDB instance which currently stores simple data like the ID of the
last tweet that it responded to and various trash-talk phrases that the bot will reply with
based on the state of the current game. Eventually, the database will also track the
statistics about users to offer more personalized responses based on this data.

Game logic is handled in ```tweet_tac_toe.py``` and ```tweet_listener.py``` monitors Twitter
for tweets that summon the bot. The bot is currently being hosted intermittently.
