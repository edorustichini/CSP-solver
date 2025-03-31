

class BinaryConstraint:
    def __init__(self, variables, constraint_func):
        """
        Binary constraint
        :param variables: tuple with variables names
        :param constraint_func: function
        """
        if len(variables) != 2:
            raise ValueError("BinaryConstraint requires exactly 2 variables")
        
        self.variables = variables
        self.constraint_func = constraint_func
    
    def is_satisfied(self, assignment):
        """
        Verifica se il vincolo è soddisfatto nell'assegnamento corrente

        :param assignment: dict {var: value}
        :return: True if constraint is satisfied, else false
        """
        # Controlla se entrambe le variabili sono assegnate
        var1, var2 = self.variables
        if var1 not in assignment or var2 not in assignment:
            return True  # if there is an unassigned var, constraint in not violated
        
        return self.constraint_func(assignment[var1], assignment[var2])
    
    def __repr__(self):
        return f"BinaryConstraint({self.variables}, {self.constraint_func.__name__})"