from constraint import BinaryConstraint


class Problem:
    def __init__(self):
        """

                :param variables: variables of the problem
                :param domains: dict of var: domain values
                :param constraints : dict of var: list of Binaryconstraints on var
         """
        self.variables = []
        self.domains = {}
        self.constraints = {}
        
    def __int__(self, variables : list, domains : dict):
        
        # TODO: nella gestione dei vincoli DEVE garantire che ogni variabile sia associata a TUTTI i vincoli nei quali la variabile è presente
        
        self.variables = variables
        self.domains = domains
        self.constraints = {} #dizionario dove per ogni variabile c'è lista di vincolo associati a quella
        
        for var in self.variables:
            if var not in self.domains:
                raise LookupError(f"Variable {var} does not have a domain")
    
    def add_variable(self, var, domain):
        """Adds variable to problem"""
        if var not in self.variables:
            self.variables.append(var)
            self.domains[var] = list(domain)
            self.constraints[var] = []
        else:
            raise ValueError(f"Variable {var} already exists")
            
    def add_constraint(self, c: BinaryConstraint):
        """Add constraint to the problem"""
        for var in c.variables:
            if var not in self.variables:
                raise LookupError(f"Variable {var} in constraint doesn't exist in problem")
            else:
                self.constraints[var].append(c)
        
    def check_assignment_consistency(self, assignment):
        """check for assignment consistency """
        for var in assignment:
            for c in assignment[var]:
                if not self.constraints[var].is_satisfied(assignment):
                    return False
        return True
    
    """------- utility functions"""
    def add_variables_same_domain(self, domain, *variables):
        """Adds list of variables sharing same domain"""
        for var in variables:
            self.add_variable(var, domain)
    
    def get_all_arcs(self):
        """Returns list of all constraints"""
        arcs = []
        for v in self.variables:
            arcs.append(self.constraints[v].copy())
        return arcs