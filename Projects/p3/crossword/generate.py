import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Loop over all variables domain:
        for variable in self.domains:
            
            domain = set(self.domains[variable])
            # calculate variable lenghth once
            length = variable.length
            
            for word in domain:
                # Remove any values that are inconsistent with a variable's length of the word.
                if len(word) != length:
                    self.domains[variable].remove(word)

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        revise = False
        olap = self.crossword.overlaps[x, y]

        # Attemp to revise x domain if x and y have overlap
        if olap:
            
            # Making a copy of x and y domain for looping
            domain_x = set(self.domains[x])
            domain_y = set(self.domains[y])
            
            # Removing values from `self.domains[x]` for which there is no
            # possible corresponding value for `y` in `self.domains[y]`
            for word_x in domain_x:
                Flag = True
                for word_y in domain_y:
                    
                    # word x and y could not be the same
                    if word_x != word_y:

                        # There is a word_y in `self.domains[y]` 
                        # consistent with word_x
                        if word_x[olap[0]] == word_y[olap[1]]:
                            Flag = False
                            break
                
                # There is no word_y in `self.domains[y]` 
                # consistent with word_x
                if Flag:
                    revise = True
                    self.domains[x].remove(word_x)           
        
        return revise

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        domains = set(self.domains)

        # If arcs is given, use the given arcs 
        if arcs:
            Arcs = arcs
        
        # If arcs is None, start with an initial 
        # queue of all of the arcs in the problem        
        else:
            Arcs = set()
            for x in domains:
                for y in domains:
                    if x == y:
                        continue
                    Arcs.add((x, y))

        while Arcs:  
            
            # Remove one arc from arcs
            arc = Arcs.pop()
            x, y = arc[0], arc[1]
            
            # Revise x domain based on the arc
            if self.revise(x, y):
                
                # Return False if domain x end up empty
                if not(self.domains[x]):
                    return False

                # Enqueue all x neighbors other than y
                for z in (self.crossword.neighbors(x) - {y}):
                    Arcs.add((z, x)) 

        return True

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Check if assignment is complete:
        # If number of assigned variables is equal to the number of variables
        if len(assignment) == len(self.domains):
            return True
        return False 

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Check if a word was already assigned to a variable
        assignment_words = []
        for var in assignment:
            assignment_words.append(assignment[var]) 
        if len(assignment_words) > len(set(assignment_words)):
            return False

        # Find all arcs in the assignment
        arcs = set()
        for x in assignment:
            for y in assignment:
                if x == y:
                    continue
                arcs.add((x, y))

        # Check arcs consistency by calling ac3
        if self.ac3(arcs):
            return True
        
        return False

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Initialize var domain and neighbors
        x = var
        domain_x = self.domains[x]
        neighbors_x = self.crossword.neighbors(x)

        # If domain_x has only one word, there is nothing to sort
        # return the word
        if len(domain_x) == 1:
            return domain_x
        
        # Initialize the words and word scores lists
        scores_x = []
        words_x = []

        for word_x in domain_x:   

            # At start, each word has zero score
            words_x.append(word_x)
            scores_x.append(0)
            
            for y in neighbors_x:

                # If y has a value, there is nothing that x can rules out
                if y in assignment:
                    continue
                
                # Find the overlap between x and y
                olap = self.crossword.overlaps[x, y]      

                # If there is not overlap, there is nothing that x can rules out
                if olap:
                    
                    # loop over domain y to finde inconsistencies between x and y
                    domain_y = self.domains[y]
                    for word_y in domain_y:
                        if word_x[olap[0]] != word_y[olap[1]]:
                            scores_x[-1] += 1

        # sort based on the on that rules out the fewest values
        ordered_words_x = [x for _, x in sorted(zip(scores_x, words_x))]

        return ordered_words_x

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        for variable in self.domains:
            
            variables = []
            lenghts = []
            
            # Find unassigned variables not already part of `assignment`.
            if not(variable in assignment):
                variables.append(variable)
                lenghts.append(len(self.domains[variable]))

            # If unassigned variables exist:
            if variables:
                
                # Find the variables with the minimum number of remaining values
                min_variables = []
                degree = []
                min_len = min(lenghts)
                
                for var in variables:
                    if len(self.domains[var]) == min_len:
                        min_variables.append(var)
                        degree.append(len(self.crossword.neighbors(var)))
                    
                # Choose the variable with the minimum number of remaining values
                if len(min_variables) == 1:
                    return min_variables[0]

                # If there is a tie, choose the variable with the highest neighbors.
                return min_variables[degree.index(max(degree))]

        return None

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if assignment is complete
        if self.assignment_complete(assignment):
            return assignment

        # Try a new variable
        variable = self.select_unassigned_variable(assignment)

        new_assignment = assignment.copy()
        
        # Try new word based on the least-constraining values heuristic 
        for word in self.order_domain_values(variable, new_assignment):
            new_assignment[variable] = word
        
            # Check new assignment consistency
            if self.consistent(new_assignment):

                result = self.backtrack(new_assignment)
                if result is not None:
                    return result

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
