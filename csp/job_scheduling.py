"""
Job-shop scheduling problems:
The variables represent the operations,
"""
from typing import override

from csp.constraint import BinaryConstraint
from csp.solver import Solver
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
        
        
    

def main():
    # Problem described in AIMA 2021 RN  chap: 6.1.2
    duration ={
        'Asse_A': 10,
        'Asse_P': 10,
        'Ruota_DA': 3,
        'Ruota_SA':3,
        'Ruota_DP': 3,
        'Ruota_SP':3,
        'Dadi_DA': 2,
        'Dadi_SA': 2,
        'Dadi_DP': 2,
        'Dadi_SP': 2,
        'Copri_DA': 1,
        'Copri_SA':1,
        'Copri_DP':1,
        'Copri_SP':1,
        'Ispezione':3
    }
    operations = list(duration.keys())
    
    jss_problem = JobShopSchedulingProblem(operations,30,  duration)
    jss_problem.add_precedence_constraint('Asse_A', 'Ruota_DA')
    jss_problem.add_precedence_constraint('Asse_P', 'Ruota_DP')
    jss_problem.add_precedence_constraint('Asse_A', 'Ruota_SA')
    jss_problem.add_precedence_constraint('Asse_P', 'Ruota_SP')
    
    jss_problem.add_precedence_constraint('Ruota_DA', 'Dadi_DA')
    jss_problem.add_precedence_constraint('Ruota_SA', 'Dadi_SA')
    jss_problem.add_precedence_constraint('Ruota_DP', 'Dadi_DP')
    jss_problem.add_precedence_constraint('Ruota_SP', 'Dadi_SP')
    
    jss_problem.add_precedence_constraint('Dadi_DA', 'Copri_DA')
    jss_problem.add_precedence_constraint('Dadi_SA', 'Copri_SA')
    jss_problem.add_precedence_constraint('Dadi_DP', 'Copri_DP')
    jss_problem.add_precedence_constraint('Dadi_SP', 'Copri_SP')
    
    jss_problem.add_disjunction_constraint('Asse_A', 'Asse_P')
    
    for op in operations:
        if op != 'Ispezione':
            jss_problem.add_precedence_constraint(op, 'Ispezione')
    
    
    solver = Solver(jss_problem)
    
    
    solutions = solver.get_all_solutions()
    
    print("Some solutions")
    num = 5
    for i, solution in enumerate(solutions[:num], start=1):
        print(f"Solution n. {i} :")
        for op, value in solution.items():
            print(f"{op} = {value}")
        print("------------------------------------------------------------------------- \n")
    print(f".... other {len(solutions) - 5} found")
    
    #TODO: SCEGLIERE UNA SOLUZIONE A COSTO MINIMO
        
main()