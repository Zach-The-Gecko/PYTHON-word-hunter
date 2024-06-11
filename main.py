# How to use:
# use the command line to input the letters on the gameboard
# from the top to bottom in rows. For example, the command
# 'python main.py abcdefghijklmnop' would be used for a boggle
# board looking like this
#       a b c d
#       e f g h
#       i j k l
#       m n o p

import sys
import math


class SupLetter():
    """
    SupLetter (super letter) is a class that has a letter and position attribute
    and has a function that will return the letters adjacent to the super letter
    """

    def __init__(self, letter, position):
        self.letter = letter
        self.position = position

    def get_adjacent_letters(self, game_board):
        """
        Returns a dictionary of all the letters that are adjacent.
        the value of the letters is a list of tuple pairs containing
        the position and direction of the letter
        """
        adjacent_letters = {}

        # Math to determine if a position is near the edge of the 4x4 gameboard
        on_top = math.floor(self.position / 4) == 0
        on_bottom = math.floor(self.position / 4) == 3
        on_right = self.position % 4 == 3
        on_left = self.position % 4 == 0

        # lists all the possible distances that when added to the letter's
        # position, will return the position of an adjacent letter. also equivelent
        # to direction because each distances corrosponds to a different direction
        adjacent_letters_index_differences = [-5, -4, -3, -1, 1, 3, 4, 5]

        # Removes the directions that collide with the edge of the board
        if on_top or on_left:
            adjacent_letters_index_differences.remove(-5)
        if on_top:
            adjacent_letters_index_differences.remove(-4)
        if on_top or on_right:
            adjacent_letters_index_differences.remove(-3)
        if on_right:
            adjacent_letters_index_differences.remove(1)
        if on_right or on_bottom:
            adjacent_letters_index_differences.remove(5)
        if on_bottom:
            adjacent_letters_index_differences.remove(4)
        if on_bottom or on_left:
            adjacent_letters_index_differences.remove(3)
        if on_left:
            adjacent_letters_index_differences.remove(-1)

        for difference in adjacent_letters_index_differences:
            adjacent_super_letter = game_board[self.position + difference]

            # Condenses the letters so each letter is a key and
            # nothing gets overwritten
            if adjacent_super_letter.letter in adjacent_letters:
                adjacent_letters[adjacent_super_letter.letter].append(
                    (adjacent_super_letter.position, difference))
            else:
                adjacent_letters[adjacent_super_letter.letter] = [
                    (adjacent_super_letter.position, difference)]

        return adjacent_letters


class Pathway:
    """
    has attributes of previous positions (history) and a list
    of directions (path). has a function that generates a new
    history and path for adjacent letters on the superboard
    """

    def __init__(self, history, path):
        self.history = history
        self.path = path

    def get_next_layer_deep(self, game_board, letter):
        """
        Returns a list of tuple pairs that contain
        the position and direction of the next letter
        Parameters: the gameboard and the desired letter
        """
        if letter in (adjacent_letters := game_board[self.history[-1]].get_adjacent_letters(game_board)):
            children = []
            for position, direction in adjacent_letters[letter]:

                # Checks if the letter has already been used in the history
                if not position in self.history:
                    history = self.history[:]
                    path = self.path[:]

                    history.append(position)
                    path.append(direction)

                    children.append((history, path))

            return children
        return []


def does_word_work(word, sup_game_board):
    """
    accepts a word and the game board, returns a path object
    if the word can be used in a word hunt game, otherwise
    returns false
    """
    # The following code loops through the gameboard and tests to see
    # if the first letter of the word matches any of the letters
    # if it does, a new Pathway object is created and added to the
    # pathways array
    pathways = []
    for sup_letter in sup_game_board:
        if word[0] == sup_letter.letter:
            pathways.append(Pathway([sup_letter.position], []))

    # Loops through the indexes of the word we're testing, checks
    # if we are at the end of the word, and then for each
    # letter it uses the pathways initially generated in the previous
    # loop to get the letters adjacent to the letter we are currently on
    # and stores the data in a new array called current_pathways.
    for current_letter_index in range(0, (length_of_word := len(word))):
        current_pathways = []
        for pathway in pathways:
            if current_letter_index < length_of_word - 1:
                if (branches := pathway.get_next_layer_deep(sup_game_board, word[current_letter_index + 1])):
                    for branch in branches:
                        current_pathways.append(Pathway(branch[0], branch[1]))

        # if there are no more pathways for the word to follow, that either
        # means that we are at the end of the word, or that we could not complete
        # the word. if we are at the end of the word we add the word to the pathway
        # object and return the path as the result, otherwise we return false
        if not current_pathways:
            if current_letter_index == length_of_word - 1:
                pathways[0].word = word
                return pathways[0]
            return False

        # Sets the newly generated form of pathways to be the next set of pathways
        # that my script will iterate over
        pathways = current_pathways[:]


user_input = sys.argv[1]

dictionary_arr = open("dictionary.txt", "r").read().lower().split("\n")

# Genereates a gameboard where instead of letters, 'super letters' are used
game_board = []
for index, letter in enumerate(user_input):
    game_board.append(SupLetter(letter, index))

valid_words = []

for word in dictionary_arr:
    if (result := does_word_work(word, game_board)):
        valid_words.append(result.word)

print(sorted(valid_words, key=len)[::-1])
