from constraint import Constraint


class Problem:
    def __init__(self):
        """
        variables: variables of the problem
        curr_domains: dict of var:domain values
        constraints : dict of var:list of Constraints on var
        
        Must initialize the problem first, and then add variables and constraints
        """
        self.variables = []
        self.domains = {}
        self.constraints : dict[any: Constraint]= {}
    
    def add_variable(self, var, domain):
        """Adds var and its domain to problem"""
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
        """
        Checks for assignment consistency by checking if every constraint for assigned variables is satisfied
        """
        for var in assignment:
            for constraint in self.constraints[var]:
                if not constraint.is_satisfied(assignment):
                    return False
        return True
    

    def add_variables_same_domain(self, domain, variables : list):
        """
        Adds list of variables sharing same domain to the problem
        """
        for var in variables:
            self.add_variable(var, domain)