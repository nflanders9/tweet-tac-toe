"""
twitter.py
Nick Flanders

Handles communication with the Twitter API for playing Tic Tac Toe
based on mentions of the bot
"""
__author__ = 'Nick Flanders'
import os
import re
from twitter import *
from credentials import *
from tweet_tac_toe import *

# set the last tweet ID that was used if there is one
if os.path.exists("last_id.txt"):
    with open("last_id.txt", 'r') as doc:
        since_id = int(doc.readline())
else:
    since_id = 0

api = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET))
results = api.search.tweets(q="@TweetTacToeBot", since_id=since_id)

for tweet in results['statuses']:
    text = tweet['text']
    sanitized = re.search(r'\[.+\]', text, re.DOTALL).group(0)
    if sanitized is not None:
        game = GameModel.parse_board(sanitized)
        game.play()
        print(game)
        api.statuses.update(
            status="Your move:\n\n" + str(game) + "\n#TweetTacToe",
            in_reply_to_status_id=tweet['id'])

# record the last found ID to start the next cycle
if len(results['statuses']) > 0:
    with open("last_id.txt", 'w') as doc:
        doc.write(str(results['statuses'][0]['id']))

