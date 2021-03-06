"""
Contains solvers to nearest, furthest relations
"""
class MatrixSolver:
    """
    Build relation matrix over data, populating with key_f\n
    key: function converting entry to comparable value
    """
    def __init__(self, key_f=(lambda x,y: x-y), symmetry=False):
        self.matrix = []
        self.key = key_f
        self.symmetry = symmetry

    def solve(self, data):
        """
        Build solution matrix\n
        Accepts a 1-dimensional list
        """
        elem = lambda i,j: (self.key(data[i], data[j]) if i != j else float('nan'))
        if self.symmetry:
            # Matrix is symmetrical and can be optimized
            self.matrix = [[None for c in range(0,len(data))] for r in range(0,len(data))]
            for r in range(0,len(data)):
                for c in range(r,len(data)):
                    self.matrix[r][c] = elem(r, c)
                    self.matrix[c][r] = self.matrix[r][c]
        else:
            self.matrix = [[elem(r, c) for c in range(0,len(data))] for r in range(0,len(data))]
        return self

    def max(self):
        """
        Get maximum value index in each row
        """
        # workaround: first element cannot be nan
        # otherwise it's always returned as max
        self.matrix[0][0] = float('-inf')
        return [row.index(max(row)) for row in self.matrix]

    def min(self):
        """
        Get minimum value index in each row
        """
        # workaround: first element cannot be nan
        # otherwise it's always returned as min
        self.matrix[0][0] = float('inf')
        return [row.index(min(row)) for row in self.matrix]
