from problem import Problem

class Solver:
    def __init__(self, csp : Problem):
        self.csp = csp
        # TODO: controlla prima che sia un minimo formato: ovvero ci siano variabile ecc
        self.solutions = []
    
    def assign(self, var, val, assignment : dict):
        """Add var to assignment"""
        assignment[var] = val
    
    def mrv(self, assignment):
        """Implementation of MRV heuristic for the choice of unassigned var to process"""
        unassigned_vars = [v for v in self.csp.variables if v not in assignment]
        
        choice = min(unassigned_vars, key=lambda var: len(var.domain))
        # FIXME: aggiungere degree heuristic in casi di parità
        return choice
    
    def order_domain_values(self, var, assignment):
        """"""
        return self.csp.domains[var]
    
    def neighbours(self, var):
        neighbours = []
        for c in self.csp.constraints[var]:
            for v in c.variables:
                if v is not var:
                    neighbours.append(v)
        return neighbours
    
    def backtracking_search(self) -> list:
        """
        Returns all solutions for the problem
        """
        self._backtracking({})
        return self.solutions
    
    def _backtracking(self, assignment :dict):
        """assignemnt is a dict of var assigned"""
        
        if self._check_assignment_complete(assignment):
            new_solution = assignment.copy()
            self.solutions.append(new_solution) # adds solution to solutions list
            return new_solution
        
        var = self.mrv(assignment)
        
        for value in self.order_domain_values(var, assignment):
            if self.value_consistent(var, value, assignment):
                assignment[var] = value
                
                success, inferences = self.mac(var, assignment) # inferences in a subset of problem.domains
                
                if success:
                    self.add_inferences(inferences)
                    result = self._backtracking(assignment)
                    if result is not None:
                        return result
                    self.remove_inferences(inferences)
                    
            assignment.pop(var)
        return None
        
    def value_consistent(self, var, val, assignment) -> bool:
        for c in self.csp.constraints[var]:
            assignment[var] = val
            if not self.csp.check_assignment_consistency(assignment):
                return False
        return True
    
    
    
    def mac(self, var, assignment: dict) -> [bool, list]:
        """
        MAC algorith
        Return list of removed values from variables domains.
        """
        
        neighbours = self.neighbours(var)
        unassigned_neighbours = [v for v in neighbours if v not in assignment]
        queue = [] # read AC-3 to understand what it contains
        for c in self.csp.constraints[var]:
            for v in c.variables:
                if v != var and v in unassigned_neighbours:
                    queue.append((var,v, c))
        
        not_fail, inferences = self.AC_3(queue)
        
        return not_fail, inferences
    
    def AC_3(self, queue=None):
        """
        AC-3 algorithm for arc consistency:
        - returns (False, None) if there's inconsitency
        - returns (True, inferences) where "inferences" is a dict with values removed from variables domains
        
        param:
        - queue:a list of tuples that contains the variables of the arc and the constraint between them
        
        """
        inferences = {}
        
        if queue is None:
            # initializes queue with all arcs;
            queue = []
            for x in self.csp.variables:
                for constraint in self.csp.constraints[x]: #there could be multiple constraints between two variables
                    y = [var for var in constraint.variables if var != x][0]
                    queue.append((x,y,constraint))
                    
        while queue:
            xi,xj, constraint = queue.pop(0)
            
            inferences = self.revise(xi,xj, constraint, inferences)
            if inferences:
                if len(self.csp.domains[xi]) == len(inferences[xi]):
                    #if same length, xi domain will be reduced to {} after adding inferences
                    return False, None
                
                for xk in self.csp.variables:
                    if xk != xi and xk != xj:
                        for c  in self.csp.constraints[xk]:
                            if xi in c.variables:
                                queue.append((xk,xi, c))
        return True, inferences
        
    def revise(self, xi, xj, constraint, inf):
        """
        Adds values to be removed in "inf", a dict var: values removed
        """
        consistent : bool = True
        for x in self.csp.domains[xi]:
            count = 0
            for y in self.csp.domains[xj]:
                if not constraint.is_satisfied({xi:x, xj: y}):
                    consistent = False
            if not consistent:
                inf[xi].append(x)
        return inf
            
    def add_inferences(self, inf):
        """
        Adds inferences (inf) removing values from variables domains
        :param inf:
        :return:
        """
        for var in inf:
            for value in inf[var]:
                # TODO: gestire caso in cui value non è presente nel dominio con eccezzioni
                self.csp.domains[var].remove(value)
    
    def remove_inferences(self, inf):
        """
        Restore domains as they were before inference operation
        """
        for var in inf:
            for value in inf[var]:
                if value not in self.csp.domains[var]:
                    self.csp.domains[var].append(value)
        
    def _check_assignment_complete(self, assignment) -> bool:
        complete = False
        if len(assignment)==len(self.csp.variables):
            complete  = True
        return complete
        
        
    