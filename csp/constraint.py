
class Constraint:
    def __init__(self, variables : set):
        #FIXME: forza la presenza di vincoli binari, o al massimo unari, perché influenza il backtracking
        self.variables = variables
        
    def is_satisfied(self, assignment) -> bool:
        """ Check if the constraint is satisfied with the (partial) assignent on the constrained values"""
        raise NotImplementedError
