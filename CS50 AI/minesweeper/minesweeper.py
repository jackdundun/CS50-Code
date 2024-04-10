import itertools
import random
import copy

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """

        if len(self.cells) == self.count:
            return self.cells



    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells


    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.


        """
        # take the sentence.mark_mine method
        #this is a item in a list
        #check and see if the item is equal to the cell
        if set(cell).issubset(set(self.cells)):
            self.cells.remove(cell)
            self.count = self.count - 1
        return self


    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if set(cell).issubset(set(self.cells)):
            self.cells.remove(cell)
        return self






class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)



    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """

        # mark the cell as a move that has been made
        self.moves_made.add(cell)
        # marking it as safe
        self.safes.add(cell)

        #convert tuplet to possible cells
        #initialising the list
        pos_choices = []
        # creating the tuples
        for i in range(3):
            for j in range(3):
                tuple_add = (cell[0] + i - 1, cell[1] + j - 1)
                pos_choices.append(tuple_add)
        # using list comprehension to remove any tuples outside the range and then converting the list into a set
        pos_choices = set([item for item in pos_choices if (item[0] > -1 and item[1] > -1) and (item[0] < 8 and item[1] < 8)])
        # removing any known safe cells from the list to cut the size down
        pos_choices = set([item for item in pos_choices if item not in self.safes])
        # removing any cells known to be mines
        pre_length = len(pos_choices.copy())
        pos_choices = set([cell for cell in pos_choices if cell not in self.mines])
        post_length = len(pos_choices)
        count = count - (pre_length - post_length)
        pos_choices.add(cell)


        new_sent = Sentence(pos_choices, count)
        self.knowledge.append(new_sent)



        #removing any known safes/mines from the sentences
        for sentence in self.knowledge:
            if sentence.count == 0:
                sentence_copy = sentence.cells.copy()
                for cell in sentence_copy:
                    self.mark_safe(cell)
            if sentence.count == len(sentence.cells) and (len(sentence.cells) != None):
                sentence_copy = sentence.cells.copy()
                for cell in sentence_copy:
                    self.mark_mine(cell)


        for sentence in self.knowledge:
            cells_copy = sentence.cells.copy()
            for cell in cells_copy:
                if cell in self.safes:
                    sentence.cells.remove(cell)

        for sentence in self.knowledge:
            cells_copy = sentence.cells.copy()
            for cell in cells_copy:
                if cell in self.mines:
                    sentence.cells.remove(cell)
                    sentence.count -= 1


        for sen1 in self.knowledge:
            for sen2 in self.knowledge:
                if sen1 == sen2:
                    continue
                elif len(sen1.cells) or len(sen2.cells) == 0:
                    continue
                elif sen1.cells.issubset(set(sen2.cells)):
                        new_choice = sen2.cells.difference(sen1.cells)
                        new_count = sen2.count - sen1.count
                        new_sent = Sentence(new_choice, new_count)
                        if new_sent not in self.knowledge:
                            self.knowledge.append(new_sent)

                elif sen2.cells.issubset(set(sen1.cells)):
                    new_choice = sen1.cells.difference(sen2.cells)
                    new_count = sen1.count - sen2.count
                    new_sent = Sentence(new_choice, new_count)
                    if new_sent not in self.knowledge:
                        self.knowledge.append(new_sent)


    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        # Keep track of which cells have been clicked on
        moves_made_copy = copy.deepcopy(self.moves_made)
        safes_copy = copy.deepcopy(self.safes)

        safe_moves = safes_copy.difference(moves_made_copy)
        if len(safe_moves) > 0:
            return safe_moves.pop()
        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        random_choices = []
        # creating the tuples
        for i in range(8):
            for j in range(8):
                tuple_add = (i, j)
                random_choices.append(tuple_add)

        random_choices = set([item for item in random_choices if (item[0] > -1 and item[1] > -1) and (item[0] < 8 and item[1] < 8)])

        random_choices = random_choices.difference(self.mines)
        random_choices = random_choices.difference(self.moves_made)
        if len(random_choices) >0:
            random_choices = list(random_choices)
            return random.choice(random_choices)
        else:
            return None