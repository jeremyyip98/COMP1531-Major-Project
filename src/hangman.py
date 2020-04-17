'''
COMP1531 Iteration 3
Hangman
Jeffrey Yang z5206134
'''
import requests
from database import list_of_channels
from random import randint

site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
response = requests.get(site)
dictionary = response.content.splitlines()

stages = ['\n\n\n\n_________\nFive tries left',
'|\n|\n|\n|\n|_________\nFour tries left',
'_______\n|\n|\n|\n|\n|_________\nThree tries left',
'_______\n|     O\n|   \n|\n|\n|_________\nTwo tries left',
'_______\n|     O\n|   /|\ \n|     \n|\n|_________\nOne try left',
'_______\n|     O\n|   /|\ \n|   \n|    /\ \n|_________\nGame over!']


def reset_hangman(channel_id):
    '''Resets the state of hangman in a channel.'''
    global list_of_channels
    for channel in list_of_channels:
        if channel['channel_id'] == channel_id:
            channel['the_word'] = ""
            channel['current_progress_list'] = []
            channel['current_progress_word'] = ""
            channel['guessed_letters_list'] = []
            channel['incorrect_letters_list'] = []

def start_game(channel_id):
    '''Starts a game of hangman in a channel. Overrides any existing game.'''
    reset_hangman(channel_id)
    global list_of_channels
    for channel in list_of_channels:
        if channel['channel_id'] == channel_id:
            channel['the_word'] = dictionary[randint(0, len(dictionary))].decode("utf-8").lower()
            for i in range(len(channel['the_word'])):
                channel['current_progress_list'].append("_")
                channel['current_progress_word'] = "".join(channel['current_progress_list'])
        return f"A game of hangman has started\n {channel['current_progress_word']}"

def make_guess(guess, channel_id):
    '''A user guesses a letter. The response they get is based on the state of the game.'''
    global list_of_channels
    for channel in list_of_channels:
        if channel['channel_id'] == channel_id:
            if channel['current_progress_word'] == channel['the_word']:
                return "You have already won. Please start a new game"
            if len(channel['incorrect_letters_list']) == 6:
                return "You have already lost. Please start a new game"
            for letter in channel['guessed_letters_list']:
                if letter == guess:
                    return f"You have already tried this letter\n {channel['current_progress_word']}\nIncorrect:{channel['incorrect_letters_list']}"
            found = False
            channel['guessed_letters_list'].append(guess)
            for i, letter in enumerate(channel['the_word']):
                if letter == guess and channel['current_progress_list'][i] != guess:
                    channel['current_progress_list'][i] = letter
                    channel['current_progress_word'] = "".join(channel['current_progress_list'])
                    found = True
            if channel['current_progress_word'] == channel['the_word']:
                return f"Congratulations!, {channel['the_word']} was the word!"
            if found:
                return f"{channel['current_progress_word']}\nIncorrect:{channel['incorrect_letters_list']}"
            channel['incorrect_letters_list'].append(guess)

            return f"{guess} is not part of the word!\n {stages[len(channel['incorrect_letters_list'])-1]}\n{channel['current_progress_word']}\nIncorrect:{channel['incorrect_letters_list']}"
