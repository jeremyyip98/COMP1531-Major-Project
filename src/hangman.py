import requests
from database import list_of_channels
from random import randint

site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = requests.get(site)
dictionary = response.content.splitlines()


def reset_hangman(channel_id):
    global list_of_channels
    for channel in list_of_channels:
        if channel['channel_id'] == channel_id:
            channel['the_word'] = ""
            channel['current_progress_list'] = []
            channel['current_progress_word'] = ""
            channel['guessed_letters_list'] = []

def start_game(channel_id):
    '''starts a game of hangman in a channel'''
    reset_hangman(channel_id)
    global list_of_channels
    for channel in list_of_channels:
        if channel['channel_id'] == channel_id:
            channel['the_word'] = dictionary[randint(0, len(dictionary))].decode("utf-8").lower()
            for i in range(len(channel['the_word'])):
                channel['current_progress_list'].append("_")
                channel['current_progress_word'] = "".join(channel['current_progress_list'])
    return "A game of hangman has started"

def make_guess(guess, channel_id):
    '''guesses a letter'''
    global list_of_channels
    for channel in list_of_channels:
        if channel['channel_id'] == channel_id:
            for letter in channel['guessed_letters_list']:
                if letter == guess:
                    return "You have already tried this letter"
            found = False
            for i, letter in enumerate(channel['the_word']):
                if letter == guess and channel['current_progress_list'][i] != guess:
                    channel['current_progress_list'][i] = letter
                    channel['current_progress_word'] = "".join(channel['current_progress_list'])
                    found = True
            if channel['current_progress_word'] == channel['the_word']:
                return f"Congratulations!, {channel['the_word']} was the word!"
            if found:
                return channel['current_progress_word']
            channel['guessed_letters_list'].append(guess)
            return f"{guess} is not part of the word!"
