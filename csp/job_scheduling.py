from constraint import BinaryConstraint
from problem import Problem

class JobShopSchedulingProblem(Problem):
    def __init__(self,  operations : list, max_time : int, operation_durations : dict):
        """
        :param operations: List of operations to be scheduled; they represent the variables of the problem, and their assigned value is the time when the operation starts
        :param max_time: Maximum time to complete all the operations
        :param operation_durations: Maps each operation to its duration
        """
        super().__init__()
        self.operation_duration = operation_durations
        for var in self.operation_duration:
            if self.operation_duration[var] is None:
                raise LookupError(f"{var} must have a duration")
            
        for op in operations:
            max_start = max_time - operation_durations[op]
            domain = list(range(1, max_start +1)) # for this problem, the domains for every variabile is the integers int [1, maxtime - their duration]
            self.add_variable(op, domain)

    def add_precedence_constraint(self, before, after):
        """
        Adds constraint "operation1 must finish before operation2" to the problem
        :param before: first operation
        :param after: second operation
        :return: None
        """
        x : int = self.operation_duration[before]
        func = lambda a,b : a + x <= b
        c = BinaryConstraint([before, after], func)
        self.add_constraint(c)
        
    def add_disjunction_constraint(self, opA, opB):
        """
        Adds constraint "A and B can't overlap" that translates to "A must finish before B OR B must finish before A"
        """
        x = self.operation_duration[opA]
        y = self.operation_duration[opB]
        func =  lambda a,b : (a + x<= b) or (b + y <= a)
        c = BinaryConstraint([opA, opB], func)
        self.add_constraint(c)