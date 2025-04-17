"""
Job-shop scheduling problems:
The variables represent the operations,
"""
from constraint import BinaryConstraint
from problem import Problem

class JobShopSchedulingProblem(Problem):
    def __init__(self,  operations : list, max_time : int, operation_durations : dict, preprocess:bool = True):
        """
        :param operations: List of operations to be scheduled; they represent the variables of the problem, and their assigned value is the time when the operation starts
        :param max_time: Maximum time to complete all the operations
        :param operation_durations: Maps each operation to its duration
        :param preprocess: Boolean to indicate if simple preprocessing must be performed when the problem is created
        """
        super().__init__()
        domain = [i + 1 for i in range(max_time)] # for this problem, the domains for every variabile is the integers int [1, maxtime]
        self.add_variables_same_domain(domain=domain.copy(), variables=operations)
        
        self.operation_duration = operation_durations
        for var in self.operation_duration:
            if self.operation_duration[var] is None:
                raise LookupError(f"{var} must have a duration")
            
        if preprocess:
            self.simple_inference()
    
    def simple_inference(self):
        """
        For the problem described in AIAMA 6.1.2: removes impossible values, e.g: if op1 has x duration, and the max_time is Y, then op1 cannot have values > Y - x
        """
        for var, duration in self.operation_duration.items():
            for i in range(duration):
                self.curr_domains[var].pop()
    
    def add_precedence_constraint(self, operation1, operation2):
        """
        Adds constraint "operation1 must finish before operation2" to the problem
        :param operation1: first operation
        :param operation2: second operation
        :return: None
        """
        x : int = self.operation_duration[operation1]
        func = lambda a,b : a + x <= b
        c = BinaryConstraint([operation1, operation2], func)
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