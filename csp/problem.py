from typing import overload

from constraint import Constraint, BinaryConstraint


class Problem:
    def __init__(self):
        """
        variables: variables of the problem
        domains: dict of var: domain values
        constraints : dict of var - list of Constraints on var
        
        Must initialize the problem first, and then add variables and constraints
        """
        self.variables = []
        self.domains = {} # TODO: forse cambiare questo in curr_domain (per indicare domains attuali, e aggiungere attributo initial_domain avere sempre in memoria una copia dei domini iniziali
        self.constraints : dict[any: Constraint]= {} #dizionario dove per ogni variabile c'è lista di vincolo associati a quella
    
    def add_variable(self, var, domain):
        """Adds variable to problem"""
        if var not in self.variables:
            self.variables.append(var)
            self.domains[var] =domain.copy()
            self.constraints[var] = []
        else:
            raise ValueError(f"Variable {var} already exists")
            
    def add_constraint(self, c: Constraint):
        """
        Add constraint to the problem; the constraint will be added to all the variables involved
        """
        for var in c.variables:
            if var not in self.variables:
                raise LookupError(f"Variable {var} in constraint not defined in problem")
            else:
                self.constraints[var].append(c)
        
    def check_assignment_consistency(self, assignment):
        """checks for assignment consistency """
        for var in assignment:
            for constraint in self.constraints[var]:  # constraints è già una lista di BinaryConstraint
                if not constraint.is_satisfied(assignment):
                    return False
        return True
    
    """------- utility functions"""
    def add_variables_same_domain(self, domain, variables : list): # TODO: capire se usare *args o lista
        """Adds list of variables sharing same domain"""
        for var in variables:
            self.add_variable(var, domain)