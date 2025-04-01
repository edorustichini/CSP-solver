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
        if var1 not in assignment or var2 not in assignment:
            return True  # if there's an unassigned var, constraint is always satisfied
        
        return self.constraint_func(assignment[var1], assignment[var2])



class PrecedenceConstraint(BinaryConstraint):
    """
    Precedence constraint between two variables for job-shop scheduling problems
    """
    def __init__(self, first ,second, first_duration : int):
        precedence = lambda a,b : a + first_duration <= b
        super().__init__([first, second], precedence)
        
#FIXME: NON HA SENSO
class DisjunctiveConstraint(BinaryConstraint):
    """
    Constraint for shared variable:
    Operations A must finish before B, or B must finish before A
    """
    def __init__(self, varA, varB, durationA, durationB):
        precedence = lambda a,b, duration : a + duration <= b
        super().__init__([varA, varB], precedence)

   # FIXME: forse possibile farlo chiamando is_satisfied di BinaryConstraint
    @override
    def is_satisfied(self, assignment) -> bool:
        # perché cambia solo il valore di ritorno
        var1, var2 = self.variables
        if var1 not in assignment or var2 not in assignment:
            return True  # if there's an unassigned var, constraint is always satisfied
        
        # FIXME: NON VA BENE
        return self.constraint_func(assignment[var1], assignment[var2]) or self.constraint_func(assignment[var2], assignment[var1])
