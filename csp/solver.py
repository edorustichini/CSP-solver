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
        unassigned_vars = [v for v in assignment if assignment[v] is None]
        
        choice = min(unassigned_vars, key=lambda var: len(self.csp.domains[var]))
        # FIXME: aggiungere degree heuristic in casi di parità
        return choice
    
    def order_domain_values(self, var, assignment : dict) -> list:
        """
        Heuristic for orderubg of domain values
        :param var:
        :param assignment:
        :return: list of value ordered with the heuristic logic
        """
        return list(self.csp.domains[var])
    
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
        assignment = {var: None for var in self.csp.variables}
        self._backtracking(assignment)
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
                    if result is None:
                        self.remove_inferences(inferences)
                    
            assignment[var] = None
        return None # fail
        
    def value_consistent(self, var, val, assignment) -> bool:
        for c in self.csp.constraints[var]:
            assignment[var] = val
            if not c.is_satisfied(assignment):
                return False
        return True
    
    def mac(self, var, assignment: dict) -> [bool, list]:
        """
        MAC algorithm - Restituisce (success, inferences)
        """
        neighbours = self.neighbours(var)
        unassigned_neighbours = [v for v in neighbours if assignment[v] is None]
        queue = []
        
        for c in self.csp.constraints[var]:
            for v in c.variables:
                if v != var and v in unassigned_neighbours:
                    queue.append((var, v, c))
        
        return self.AC_3(queue)
    
    def AC_3(self, queue=None):
        if queue is None:
            queue = []
            for x in self.csp.variables:
                for constraint in self.csp.constraints[x]:
                    y = [var for var in constraint.variables if var != x][0]
                    queue.append((x, y, constraint))
        
        inferences = {var: [] for var in self.csp.variables}
        
        while queue:
            xi, xj, constraint = queue.pop(0)
            
            removed_values = self.revise(xi, xj, constraint)
            if removed_values:
                inferences[xi].extend(removed_values[xi])
                
                if not self.csp.domains[xi]:
                    return False, None
                
                for xk in self.neighbours(xi):
                    if xk != xj:
                        for c in self.csp.constraints[xk]:
                            if xi in c.variables:
                                queue.append((xk, xi, c))
        
        return True, inferences
    
    def revise(self, xi, xj, constraint):
        inf = {}
        for x in self.csp.domains[xi].copy():
            consistent = False
            for y in self.csp.domains[xj]:
                if constraint.is_satisfied({xi: x, xj: y}):
                    consistent = True
                    break
            
            if not consistent:
                if xi not in inf:
                    inf[xi] = []
                if x not in inf[xi]:  #
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
                print(f"Rimosso {value} dal dominio di {var}")
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
        for v in self.csp.variables:
            if assignment[v] is None:
                return False
        return True
        
        
    