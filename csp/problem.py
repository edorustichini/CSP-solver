'''
Definizione di classe per problema CSP generico
'''
from collections.abc import Hashable # TODO: controlla se questo o hashable in typing

from solver import Solver
from constraint import Constraint

class Variable:
    def __init__(self, name : str, domain : list):
        self.name = name
        self.domain = domain

class Problem:
    def __init__(self):
        self.variables = []
        self.constraints  = []
        
    
    def check_consistency(self, assignment):
        """check for assignment consistency """
        for constraint in self.constraints:
            consistent : bool= constraint.is_satisfied(assignment)
            if not consistent:
                return False
        return True
    
    def add_variable(self, var : Variable):
        self.variables.append(var)
    
    def add_constraint(self, c : Constraint):
        self.constraints.append(c)
        
    def get_all_constraints(self):
        return self.constraints
        
        