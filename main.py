import math


class SupLetter():

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

            # Catches duplicates where adjacent letters repeats, otherwise
            # It just creates a new array
            if adjacent_super_letter.letter in adjacent_letters:
                adjacent_letters[adjacent_super_letter.letter].append(
                    (adjacent_super_letter.position, difference))
            else:
                adjacent_letters[adjacent_super_letter.letter] = [
                    (adjacent_super_letter.position, difference)]

        return adjacent_letters


class Pathway:
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

                if not position in self.history:
                    history = self.history[::]
                    path = self.path[::]

                    history.append(position)
                    path.append(direction)

                    children.append((history, path))

            return children
        return []


def does_word_work(word, sup_game_board):
    pathways = []
    for index in range(0, len(sup_game_board)):
        if word[0] == sup_game_board[index].letter:
            pathways.append(Pathway([index], []))

    for letter_index in range(0, len(word)):
        new_pathways = []
        for pathway in pathways:
            if letter_index < len(word) - 1:
                if (new_paths := pathway.get_next_layer_deep(sup_game_board, word[letter_index+1])):
                    for new_path in new_paths:
                        new_pathways.append(Pathway(new_path[0], new_path[1]))

        if not new_pathways:
            if letter_index == len(word)-1:
                pathways[0].word = word
                return pathways[0]
            return False

        pathways = new_pathways[::]


dictionary = open("dictionary.txt", "r").read().lower().split("\n")

user_input = "jdoeuvnmakfioshj"

game_board = []

for index, letter in enumerate(user_input):
    game_board.append(SupLetter(letter, index))

valid_words = []

for word in dictionary:
    if (result := does_word_work(word, game_board)):
        valid_words.append(result.word)

print(sorted(valid_words, key=len)[::-1])
