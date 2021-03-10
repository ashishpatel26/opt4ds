""" 
   Algoritmo del simplesso per problema primale:
    
     max sum(c[j] * x[j]  for j in 1..n)
    s.t. sum(- A[i][j] * x[j] for j in 1..n) <= b[i]  for i in 1..m
         x[j] >= 0  for j in 1..n
         
    Autore: Bernardo Forni, bernardo.forni01@universitadipavia.it, (C) 2020.
    
"""

import numpy as np

# Parameters
OptimalityTol  = 1e-06
FeasibilityTol = 1e-06

# Main class
class LinearProblem:
    def __init__(self, c, A, b):
        """ Default costructor """
        self.not_base = list(range(1, len(c)+1))  # j = 1..n
        self.base = list(range(len(c)+1, len(c)+len(b)+1))  # n+i, i = 1..m
        
        self.D = np.row_stack(([0] + c, np.column_stack((b, A)))).astype(float)  # (m+1)*(n+1) matrix


    def __str__(self):
        """ Print current dictionary values """
    
        str = 'Current Basic Solution: '
        
        for x in list(range(1, len(self.not_base)+1)):
            str += f'x_{x}=0, ' if x in self.not_base else f'x_{x}={self.D[self.base.index(x)+1,0]:g}, '
        str += f'z={-self.D[0][0]:g}'
        
        return str
    
    
    def get_obj(self):
        return -self.D[0,0]


    def check_optimality(self):
        """ Check if the current basic solution is optimal """
        return not any(c > OptimalityTol for c in self.D[0, 1:])
    
    
    def check_feasibility(self):
        """ Check if the current basic solution is feasible """  
        return not any(c < -FeasibilityTol for c in self.D[1:, 0])
    

    def select_entering(self):
        """ Select an entering variable with largest c[j]. Return index k """   
        return 1 + np.argmax(self.D[0, 1:])
        

    def select_leaving(self, k):
        """ Select a leaving variable that maximize A[i][k] / b[i]. Return index h """
        # TODO: check for degenerate problem (b[h] == 0 or A[h][k] == 0)      
        return 1 + np.argmax(self.D[1:,k] / self.D[1:,0])
  
    
    def pivoting(self, k, h):
        """ Change the current dictionary according to the pivoting operations. 
            Do not return anything (void function) 
        """
        no_h = np.ones(self.D.shape[0], dtype=bool)
        no_h[h] = False
        no_k = np.ones(self.D.shape[1], dtype=bool)
        no_k[k] = False

        # pivot leaving variables
        self.D[h,k] = 1 / self.D[h,k]
        self.D[h,:][no_k] = self.D[h,:][no_k] * self.D[h,k]
        
        # pivot other variables
        self.D[np.ix_(no_h, no_k)] -= np.outer(self.D[:,k][no_h], self.D[h,:][no_k])

        # pivot entering variables
        self.D[:,k][no_h] = - self.D[:,k][no_h] * self.D[h,k]
        
        # enter, leave base
        self.not_base[k-1], self.base[h-1] = self.base[h-1], self.not_base[k-1]


    def solve(self):
        """ Using the previous functions, solve the given LP """
        
        if not self.check_feasibility():
            print('ERROR: First Basic solution must be feasible!')
            return False
        
        while not self.check_optimality():
            k = self.select_entering()
            h = self.select_leaving(k)

            print(f'Pivoting: k={k}, h={h}')
            self.pivoting(k, h)
        
        return True


def main():
    # Exercise 2.1 https://vanderbei.princeton.edu/JAVA/pivot/simple.html
    c = [6, 8, 5, 9]  # cost
    A = [[2, 1, 1, 3],
         [1, 3, 1, 2]]  # constraint coefficients
    b = [5, 3]  # RHS
    
    # Exercise 2.2
    # c = [2, 1]
    # A = [[2, 1],
    #      [2, 3],
    #      [4, 1],
    #      [1, 5]]
    # b = [4, 3, 5, 1]
    
    # solve LP problem
    LP = LinearProblem(c, A, b)
    LP.get_obj()
    LP.solve()
    LP.get_obj()
    print(LP)


if __name__ == "__main__":
    main()
