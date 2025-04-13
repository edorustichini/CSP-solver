class Constraint:
    """
    Base class representing constraint
    :param variables: variables involved
    :param constraint_func: function that represent the actual constraint on the variables
    """
    def __init__(self, variables : list, constraint_func):
        self.variables = variables
        self.constraint_func = constraint_func
    
    def is_satisfied(self, assignment) -> bool:
        """
        Verify if constrain is satisfied with the current assignment.
        :param assignment: dict {var: value}
        :return: True if constraint is satisfied, else false
        """
        raise NotImplementedError


class BinaryConstraint(Constraint):
    def __init__(self, variables, constraint_func):
        
        if len(variables) != 2:
            raise ValueError("BinaryConstraint requires exactly 2 variables")
        
        super().__init__(variables, constraint_func) #create the constraint
        
    
    def is_satisfied(self, assignment) -> bool:
        var1, var2 = self.variables
        if assignment[var1] is None or assignment[var2] is None:
            return True # If one of the vars involved is unassigned the constraint is considered satisfied
        return self.constraint_func(assignment[var1], assignment[var2])


