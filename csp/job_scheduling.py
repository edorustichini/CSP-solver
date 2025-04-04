"""
Job-shop scheduling problems:
The variables represent the operations,
"""
from csp.constraint import BinaryConstraint
from problem import Problem

class JobShopSchedulingProblem(Problem):
    def __init__(self,  operations : list, max_time : int, operation_durations : dict):
        super().__init__()
        domain = [i + 1 for i in range(max_time)]

        self.add_variables_same_domain(domain=domain.copy(), variables=operations)
        
        # every operation has a fixed duration
        self.operation_duration = operation_durations
        for var in self.operation_duration:
            if self.operation_duration[var] is None:
                raise LookupError(f"{var} must have a duration")
            
        self.simple_inference() # FIXME: capire se levarla o se metterla da altre parti
    
    
    def simple_inference(self):
        '''
        Removes impossible values. Ex: if op1 has x duration, and the max_time is Y, then op1 cannot have values > Y - x
        FIXME: agigusta questo commento
        :return:
        '''
        for var, duration in self.operation_duration.items():
            for i in range(duration):
                self.domains[var].pop()
    
    def add_precedence_constraint(self, operation1, operation2):
        '''
        Adds constraint "operation1 must finish before operation2" to the problem
        :param operation1: first operation
        :param operation2: second operation
        :return: None
        '''
        x : int = self.operation_duration[operation1]
        func = lambda a,b : a + x <= b
        c = BinaryConstraint([operation1, operation2], func) #a + c <= b
        self.add_constraint(c)
        
    def add_disjunction_constraint(self, A, B):
        """
        Adds constraint "A and B can't overlap" that translates to "A must finish before B OR B must finish before A"
        """
        x = self.operation_duration[A]
        y = self.operation_duration[B]
        func =  lambda a,b : (a + x<= b) or (b + y <= a)
        c = BinaryConstraint([A,B], func)
        self.add_constraint(c)