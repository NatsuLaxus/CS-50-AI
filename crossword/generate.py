import sys

from crossword import *
from collections import deque
import copy
import PIL

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
        # raise NotImplementedError
        # for v in self.crossword.variables:
        variables = list(self.domains.keys())
        for v in variables:
            domain = copy.deepcopy(self.domains[v])
            for d in domain:
                if len(d) != v.length:
                    self.domains[v].remove(d)
        return True

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # raise NotImplementedError
        revised = False
        d = self.crossword.overlaps[x,y]
        if d == None:
            return revised
        i = d[0]
        j = d[1]
        dom_x = list(self.domains[x])
        dom_y = list(self.domains[y])
        for x_ in dom_x:
            sol = False
            for y_ in dom_y:
                if y_[j] == x_[i]:
                    sol = True
                    break;
            if sol == False:
                self.domains[x].remove(x_)
        # for i in dom:
        #     if any(j[d[1]] == i[d[0]] for j in self.domains[y]) == False:
        #         self.domains[x].remove(i)
        #         revised = True
        return revised

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # raise NotImplementedError
        if arcs == None:
            arcs = []
            dom = list(self.domains.keys())
            for d1 in dom:
                neigh = self.crossword.neighbors(d1)
                for n in neigh:
                    if (d1,n) not in arcs and (n,d1) not in arcs:
                        arcs.append((d1,n))
            # print(arcs)
        while len(arcs)>0:
            d = arcs.pop(0)
            if d is None:
                return False
            i = d[0]
            j = d[1]
            if self.revise(i,j) == True:
                if len(self.domains[i]) == 0:
                    return False
                for z in self.crossword.neighbors(i):
                    if z != j:
                        arcs.append((z,i))
        return True


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # raise NotImplementedError
        dom = self.domains.keys()
        for d in dom:
            if d  not in assignment:
                return False
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # raise NotImplementedError
        var = assignment.keys()
        val = assignment.values()
        variables = self.domains.keys()
        all_soln = set()
        for v in variables:
            if v in assignment:    
                if assignment[v] in all_soln:
                    return False
                all_soln.add(assignment[v])
                if v in assignment:    
                    if len(assignment[v]) != v.length:
                        return False
                neigh = self.crossword.neighbors(v)
                for v2 in neigh:
                    if v2 in assignment:
                        (i,j) = self.crossword.overlaps[v,v2]
                        if assignment[v][i] != assignment[v2][j]:
                            return False
        return True

    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        l = []
        for d in self.domains[var]:
            l.append(d)
        return l
        # raise NotImplementedError

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        dom = self.domains.keys()
        size = 1000
        degree = 0
        var = None
        for d in dom:
            if d not in assignment:    
                val_domain = self.domains[d]
                count = 0
                for v in val_domain:
                    count = count+1
                neigh = self.crossword.neighbors(d)
                neigh_count = 0
                for n in neigh:
                    neigh_count = neigh_count+1
                if count<size :
                    size = count
                    var = d
                    degree = neigh_count
                elif count == size:
                    if neigh_count > degree:
                        size = count
                        var = d
                        degree = neigh_count
        return var
        # raise NotImplementedError

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # raise NotImplementedError
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var,assignment):
            new_assignment = assignment.copy()
            new_assignment[var] = value
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
