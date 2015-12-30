"""
twitter.py
Nick Flanders

Handles communication with the Twitter API for playing Tic Tac Toe
based on mentions of the bot
"""
__author__ = 'Nick Flanders'
import os
import re
import time
import pymongo
import random
from twitter import *
from credentials import *
from tweet_tac_toe import *

client = pymongo.MongoClient(MONGODB_URI)
db = client.get_database("tweet-tac-toe")
users = db['users']
last_id = db["last_id"]
interactions = db['interactions']
trash_talk = [quote['text'] for quote in interactions.find({"type": "trash_talk"})]
win_quotes = [quote["text"] for quote in interactions.find({"type": "winning"})]
tie_quotes = [quote["text"] for quote in interactions.find({"type": "tie"})]

# set the last tweet ID that was used if there is one
while True:
    since_id = last_id.find_one()['last_id']

    api = Twitter(auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET, API_KEY, API_SECRET))
    results = api.search.tweets(q="@TweetTacToeBot", since_id=since_id)

    for tweet in results['statuses']:
        text = tweet['text']
        try:
            sanitized = re.search(r'\[.+\]', text, re.DOTALL).group(0)
        except AttributeError:
            continue
        if sanitized is not None:
            try:
                game = GameModel.parse_board(sanitized)
            except ValueError:
                api.statuses.update(
                status="There's something wrong with that board. Try again, @" + str(tweet['user']['screen_name']),
                in_reply_to_status_id=tweet['id'])
                continue

            # the minimax search algorithm in its current state should never lose, so assume there was cheating if
            # this case is reached
            if game.game_over():
                api.statuses.update(
                    status="Something doesn't add up in this game, @" + str(tweet['user']['screen_name']) +
                           "\n\nNo one likes a cheater",
                    in_reply_to_status_id=tweet['id'])
            else:
                game.play()
                if game.game_over():
                    if game.check_winner() == GamePiece.EMPTY:
                        message = random.choice(tie_quotes)
                    else:
                        message = random.choice(win_quotes)
                else:
                    message = random.choice(trash_talk)
                if message[-1] == "?":
                    message = "@" + str(tweet['user']['screen_name']) + " " + message
                else:
                    message += ", @" + str(tweet['user']['screen_name'])
                api.statuses.update(
                    status=message + "\n\n" + str(game) + "\n#TweetTacToe",
                    in_reply_to_status_id=tweet['id'])

    # record the last found ID to start the next cycle
    if len(results['statuses']) > 0:
        last_id.update({"last_id": since_id}, {"last_id": results["statuses"][0]["id"]})

    time.sleep(10)

