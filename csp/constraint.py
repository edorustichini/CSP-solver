from typing import override


class Constraint:
    """
    constraint
    :param variables: tuple with variables names
    :param constraint_func: function that represent the constraint on the variables
    """
    def __init__(self, variables, constraint_func):
        self.variables = variables
        self.constraint_func = constraint_func
    
    def is_satisfied(self, assignment) -> bool:
        raise NotImplementedError


class BinaryConstraint(Constraint):
    def __init__(self, variables, constraint_func):
        
        if len(variables) != 2:
            raise ValueError("BinaryConstraint requires exactly 2 variables")
        
        super().__init__(variables, constraint_func)
        
    
    def is_satisfied(self, assignment) -> bool:
        """
        Verifica se il vincolo è soddisfatto nell'assegnamento corrente

        :param assignment: dict {var: value}
        :return: True if constraint is satisfied, else false
        """
        var1, var2 = self.variables
        if assignment[var1] is None or assignment[var2] is None:
            return True  # if there's an unassigned var, constraint is always satisfied
        
        return self.constraint_func(assignment[var1], assignment[var2])


