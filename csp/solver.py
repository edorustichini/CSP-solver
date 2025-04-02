from problem import Problem

class Solver:
    def __init__(self, csp : Problem):
        self.csp = csp
        # TODO: controlla prima che sia un minimo formato: ovvero ci siano variabile ecc
        self.solutions = []
    
    def assign(self, var, val, assignment : dict):
        """Add var to assignment"""
        assignment[var] = val
    
    def _mrv(self, assignment):
        """Implementation of MRV heuristic for the choice of unassigned var to process"""
        unassigned_vars = [v for v in assignment if assignment[v] is None]
        
        choice = min(unassigned_vars, key=lambda var: len(self.csp.domains[var]))
        # FIXME: aggiungere degree heuristic in casi di parità
        return choice
    
    def _order_domain_values(self, var, assignment : dict) -> list:
        """
        Heuristic for orderubg of domain values
        :param var:
        :param assignment:
        :return: list of value ordered with the heuristic logic
        """
        return list(self.csp.domains[var])
    
    def _neighbours(self, var):
        neighbours = []
        for c in self.csp.constraints[var]:
            for v in c.variables:
                if v is not var:
                    neighbours.append(v)
        return neighbours
    
    def get_all_solutions(self) -> list[dict]:
        """
        First calls AC_3 to reduce domains, then search the solution using backtracking based on MAC
        :return:
        """
        print("AC_3 is running .....")
        if self._AC_3() is None:
            return None
        print("Domains after AC_3")
        for var, domain in self.csp.domains.items():
            print(var + f" : {domain}")
        print("Backtracking is searching the solution...")
        solutions = self.backtracking_search()
        print("Finished!!!")
        print(f"Found {len(solutions)} solutions to the problem")
        return solutions
    
    def backtracking_search(self) -> list[dict]:
        """
        Returns all solutions for the problem
        """
        #TODO: forse da cambiare il nome di questa funzione in "get all solutions" oppure fare funzione get all solution che prima chiama AC_3 e poi fa la backtracking search
        #TODO: magari gestire caso di variabili senza vincoli che quindi possono essere "rimosse" dal problema, perché possono assumere qualsiasi valore
        assignment = {var: None for var in self.csp.variables}
        self._backtracking(assignment)
        return self.solutions
    
    
    def _backtracking(self, assignment :dict):
        """assignemnt is a dict of var assigned"""
        if self._check_assignment_complete(assignment):
            new_solution = assignment.copy()
            self.solutions.append(new_solution) # adds solution to solutions list
            return new_solution
        
        var = self._mrv(assignment)
        
        for value in self._order_domain_values(var, assignment):
            if self._value_consistent(var, value, assignment):
                assignment[var] = value
                
                success, inferences = self._mac(var, assignment) # inferences in a subset of problem.domains
                
                if success:
                    result = self._backtracking(assignment)
                    if result is None:
                        self._remove_inferences(inferences)
            
            assignment[var] = None
        return None # fail
        
    def _value_consistent(self, var, val, assignment) -> bool:
        for c in self.csp.constraints[var]:
            assignment[var] = val
            if not c.is_satisfied(assignment):
                return False
        return True
    
    def _mac(self, var, assignment: dict) -> [bool, list]:
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
        NOTA: questa implementazione non modifica i domini delle variabili, ma ritorna i valori da togliere
        :param queue:
        :return:
        """
        if queue is None:
            queue = []
            for x in self.csp.variables:
                for constraint in self.csp.constraints[x]:
                    y = [var for var in constraint.variables if var != x][0]
                    queue.append((x, y, constraint))
        
        inferences = {var: [] for var in self.csp.variables}
        
        while queue:
            xi, xj, constraint = queue.pop(0)
            
            removed_values = self._revise(xi, xj, constraint)
            if removed_values:
                inferences[xi].extend(removed_values[xi])
                
                if len(inferences[xi])==len(self.csp.domains[xi]):
                    #xi domain will be reduced to {}
                    print("There's no solution to the problem")
                    return False, None
                
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
        Adds inferences (inf) removing values from variables domains
        :param inf:
        :return:
        """
        for var in inf:
            for value in inf[var]:
                # TODO: gestire caso in cui value non è presente nel dominio con eccezzioni
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
        
        
    #TODO USARE for key, value in dict.items(): value per iterare sui dizionari, invece di fare for key in dict : dict[var]