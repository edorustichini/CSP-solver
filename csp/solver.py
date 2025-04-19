from problem import Problem

class Solver:
    def __init__(self, csp : Problem):
        self.csp = csp
    
    def get_all_solutions(self) -> list[dict]:
        """
        Returns all found solutions: performs AC-3 before searching the solution
        """
        print("Backtracking is searching the solutions...")
        self._AC_3()
        solutions = self.backtracking_search()
        print("Finished!!!")
        return solutions
    
    def backtracking_search(self) -> list[dict]:
        empty_assignment = {var: None for var in self.csp.variables} #a key for every var
        solutions = []
        self._backtracking(empty_assignment, solutions)
        return solutions
    
    def _backtracking(self, assignment :dict, solutions : list):
        """
        Performs backtracking search based on MAC and returns all solutions for the problem.
        """
        if self._check_assignment_complete(assignment):
            # adds new solution and returns it the previous call of _backtracking
            new_solution = assignment.copy()
            solutions.append(new_solution)
            return new_solution
        
        selected_var = self._mrv(assignment)
        
        for value in self._order_domain_values(selected_var, assignment):
            if self._is_value_consistent(selected_var, value, assignment):
                assignment[selected_var] = value #extend the assignment assigning value to var
                
                success, inferences = self._mac(selected_var, assignment)
                
                if success: #
                    result = self._backtracking(assignment, solutions)
                self._remove_inferences(inferences)
    
            assignment[selected_var] = None
        return None # fail
 
    def _is_value_consistent(self, var, val, assignment) -> bool:
        """
        A value is consistent if, when assigned to the var, it doesn't "break" a constraint
        """
        assignment[var] = val
        for c in self.csp.constraints[var]:
            if not c.is_satisfied(assignment):
                return False
        return True
    
    def _mrv(self, assignment):
        """
        Implementation of Minimum Remaining Values heuristic for the selection of an unassigned var to process.
        If there are multiple variables with same number of remaining values, degree heuristic is used.
        """
        unassigned_vars = [v for v in assignment if assignment[v] is None]
        
        mrv = min(len(self.csp.domains[var]) for var in unassigned_vars)
        min_vars = [var for var in unassigned_vars if len(self.csp.domains[var]) == mrv]
        
        if len(min_vars) > 1:
            return max(min_vars, key=lambda var: len(self.csp.constraints[var]))  # degree heuristic
        else:
            return min_vars[0]
    
    def _order_domain_values(self, var, assignment: dict) -> list:
        """
        Heuristic for ordering of domain values, returns list of value ordered with the heuristic logic
        """
        return list(self.csp.domains[var])  # for the example of the project's assignment it doesn't make sense to order domain values because it's requested to enumerate all solutions
    
    def _neighbours(self, var):
        """
        Finds neighbours of var in the constraint graph
        :param var:
        :return:
        """
        neighbours = []
        for c in self.csp.constraints[var]:
            for v in c.variables:
                if v is not var:
                    neighbours.append(v)
        return neighbours
    
    def _mac(self, var, assignment: dict) -> (bool, list):
        """
        MAC algorithm - Returns (success, inferences)
        """
        neighbours = self._neighbours(var)
        unassigned_neighbours = [v for v in neighbours if assignment[v] is None]
        queue = []
        
        for c in self.csp.constraints[var]:
            for v in c.variables:
                if v != var and v in unassigned_neighbours:
                    queue.append((var, v, c))
        
        return self._AC_3(queue)
        
    def _AC_3(self, queue=None):
        """
        AC-3 algorithm: if queue=None its initialized with every arc
        """
        if queue is None:
            queue = []
            for x in self.csp.variables: # add every arc of the constraint graph
                for constraint in self.csp.constraints[x]:
                    y = [var for var in constraint.variables if var != x][0]
                    queue.append((x, y, constraint))
        
        inferences = {var: [] for var in self.csp.variables} #list of values to be removed for every var => it is a subset of problem.domain
        
        while queue:
            xi, xj, constraint = queue.pop(0)
            
            removed_values = self._revise(xi, xj, constraint)
            if removed_values:
                inferences[xi].extend(removed_values[xi])
                
                if len(inferences[xi])==len(self.csp.domains[xi]):  #xi domain is reduced to {}
                    return False, {}
                    
                self._add_inferences(inferences)
                
                for xk in self._neighbours(xi):
                    if xk != xj:
                        for c in self.csp.constraints[xk]:
                            if xi in c.variables:
                                queue.append((xk, xi, c))
        return True, inferences
    
    def _revise(self, xi, xj, constraint):
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
            
    def _add_inferences(self, inf):
        """
        Adds inferences to the problem by removing values from variables domains
        """
        for var in inf:
            for value in inf[var]:
                if value in self.csp.domains[var]:
                    self.csp.domains[var].remove(value)

    def _remove_inferences(self, inf):
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