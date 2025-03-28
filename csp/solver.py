from tabnanny import check

from constraint import Constraint
from csp.problem import Variable
from problem import Problem

class Solver:
    def __init__(self, csp : Problem):
        self.csp = csp
        self.assignment : dict = {var:None for var in self.csp.variables}
  
    
    def _neighbours(self, var) -> list:
        """Return neighbouring variables (in the constraint graph) to var
           used is AC-3/MAC
        """
        neighbours = []
        for c in self.csp.constraints:
            if var in c.variables:
                neighbours += list(c.variables - {var})
        return neighbours

    
    @staticmethod
    def assign(var, val, assignment : dict):
        """Add var to assignment"""
        assignment[var] = val
    
    "--- Heuristics for variable and value---"
    def mrv(self, unassigned_vars):
        """Implementation of MRV heuristic for the choice of unassigned var to process"""
        mrv_var = min(unassigned_vars, key=lambda var: len(var.domain))
        #FIXME: aggiungere degree heuristic in casi di parità
        return mrv_var
    
    def lcv(self, assignment):
        # TODO
        pass
    
    
    
    def AC3(self,  removed_values, queue=None):
        """AC3 algorithm"""
        if removed_values is None:
            removed_values = {}
        if queue is None:
            queue = self.csp.get_all_constraints()
        
        while len(queue) != 0:
            constraint = queue.pop()
            Xi = constraint.variables[0]
            Xj = constraint.variables[1]
            if self.revise(constraint):
                if len(Xi.domain) == 0:
                    return False, {}
                neighbours = self._neighbours(Xi)
                neighbours.remove(Xj)
                for Xk in neighbours:
                    queue.append(Xk)
        
        return True, removed_values
        
        
    
    def revise(self, constraint : Constraint) -> bool:
        removed = False
        Xi, Xj = constraint.variables # FIXME: e se ci fosse un vincolo unario?
        for x in Xi.domain:
            if not self.arc_consistency(constraint, x):
                Xi.domain.remove(x)
                removed = True
        return removed
    
    def arc_consistency(self, constraint, x_value) -> bool:
        """used in revise"""
        X = constraint.variables[0]
        Y = constraint.variables[1]
        for y_value in Y.domain:
            partial_assignment = {X: x_value, Y:y_value}
            if not constraint.is_satisfied(partial_assignment):
                return False
        return True
    
    
    def mac(self, var, assignment : dict):
        """ Return list of removed values from variables domains"""
        unassigned_vars = {var for var in self.assignment if assignment[var] is None}
        neighbours = set(self._neighbours(var))
        
        inferences = None
        not_fail, inferences =  self.AC3(inferences,neighbours - unassigned_vars)[1]
        
        return not_fail, inferences
    
        
        
    