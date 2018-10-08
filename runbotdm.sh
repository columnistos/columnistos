#!/bin/sh
export TESTING='True'
export LOG_FOLDER='./logs/'
export LOG_LEVEL='DEBUG'

export TWITTER_CONSUMER_KEY=""
export TWITTER_CONSUMER_SECRET=""
export TWITTER_ACCESS_TOKEN=""
export TWITTER_ACCESS_TOKEN_SECRET=""
python columnistos_bot.py -dm
