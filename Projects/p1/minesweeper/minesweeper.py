import itertools
import random


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
        mines = set()
        for i in self.cells:
            if self.mark_mine(i):
                mines.add(i)
        return mines

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safes = set()
        for i in self.cells:
            if self.mark_safe(i):
                safes.add(i)
        return safes

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if self.count == len(self.cells):
            return True

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if self.count == 0:
            return True



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
    
    def nearby_cells(self, cell):
        
        nearby = set()
        
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                
                # Ignore the cells that are out of the board
                if i == self.height or j == self.width or i == -1 or j == -1:
                    continue
                
                # add the cell to nearby
                nearby.add((i, j))

        return nearby   

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
        
        # mark the cell as safe
        self.mark_safe(cell)

        #add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        
        sentence = Sentence(self.nearby_cells(cell), count)
        
        for cell in sentence.cells:
            if sentence.mark_safe(cell):
                self.mark_safe(cell)
            if sentence.mark_mine(cell):
                self.mark_mine(cell)

        self.knowledge.append(sentence)

        # mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        for sent in self.knowledge:

            if len(sent.cells)==0:
                self.knowledge.remove(sent)
                continue

            for cell in self.moves_made:
                if cell in sent.cells:
                    sent.cells.remove(cell)

            for cell in self.mines:
                if cell in sent.cells:
                    sent.cells.remove(cell)
                    sent.count -= 1

            for cell in self.safes:
                if cell in sent.cells:
                    sent.cells.remove(cell)
            
            for cell in sent.cells:
                if sent.mark_safe(cell):
                    self.mark_safe(cell)
                if sent.mark_mine(cell):
                    self.mark_mine(cell)

            for sent2 in self.knowledge:
                if sent2==sent:
                    continue
                if sent2.cells-sent.cells == None:
                    sentence2 = Sentence(sent.cells - sent2.cells, sent.count - sent2.count)
                    self.knowledge.append(sentence2)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        if len(self.mines) + len(self.moves_made) == self.height * self.width:
            return None
            
        for move in self.safes:
            if not(move in self.moves_made):
                return move

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        if not(self.make_safe_move()):
            
            if len(self.mines) + len(self.moves_made) == self.height * self.width:
                    return None
            
            while True:
                i = random.randrange(self.height)
                j = random.randrange(self.width)
                move = (i, j)
                if  not(move in self.mines) and not(move in self.moves_made):
                    print('move =', move)
                    return move