import time
from cpmpy import *
import numpy as np

def solve_with_cpmpy(durations, max_time, precedence_constraints, final_operation='Ispezione'):
    operations = list(durations.keys())

    start = {
        op: intvar(1, max_time -durations[op], name=f"start_{op}") for op in operations
    }
    
    model = Model() # collection of constraints over variables, it represents the CSP problem
    
    
    for before, after in precedence_constraints:
        model += (start[before] + durations[before] <= start[after])
    
    # Disjunction constraints
    a, b = 'Asse_A', 'Asse_P'
    model += ((start[a] + durations[a] <= start[b]) | (start[b] + durations[b] <= start[a]))

    for op in operations:
        if op != final_operation:
            model += (start[op] + durations[op] <= start[final_operation])
    
    def get_cost(solution):
        return solution[final_operation] + durations[final_operation]
    
    
    solutions = []

    def print_solution():
        sol = {op: start[op].value() for op in operations}
        solutions.append(sol)
        
    print("CPMpy is searching for solutions...")
    start_time = time.time()
    n_solutions = model.solveAll(display=print_solution())
    my_execution_time = time.time() - start_time

    
    if n_solutions > 0:
        #min_cost = min(get_cost(sol) for sol in solutions)
        #min_solutions = [sol for sol in solutions if get_cost(sol) == min_cost]
        print(f"\n" + 20*"--" + "CPMpy solver" + 20*"--")
        print(f"Found {n_solutions} solutions")
        #print(f"Found {len(min_solutions)} minimal cost solutions ")
        #print(f"Minimal cost: {min_cost}")
        print(f"Execution time: {my_execution_time:.3f} seconds")
        
        '''
        print("\n*** Minimum cost solution ***")
        chosen = min_solutions[0]
        for var in sorted(chosen, key=lambda x: chosen[x]):
            print(f"{var} = {chosen[var]}")
        print(f"Cost: {get_cost(chosen)}")
        '''
    
    else:
        print("No solution to the problem")
        min_cost = None
    return {
        "solutions": len(solutions) if solutions else 0,
        "min_cost":  0,
        "execution_time": my_execution_time
    }

if __name__ == "__main__":
    duration1 = {
            'Asse_A': 10,
            'Asse_P': 10,
            'Ruota_DA': 3,
            'Ruota_SA': 3,
            'Ruota_DP': 3,
            'Ruota_SP': 3,
            'Dadi_DA': 2,
            'Dadi_SA': 2,
            'Dadi_DP': 2,
            'Dadi_SP': 2,
            'Copri_DA': 1,
            'Copri_SA': 1,
            'Copri_DP': 1,
            'Copri_SP': 1,
            'Ispezione': 3
        }
    max_time1 = 30
    precedences = [
        ('Asse_A', 'Ruota_DA'),
        ('Asse_P', 'Ruota_DP'),
        ('Asse_A', 'Ruota_SA'),
        ('Asse_P', 'Ruota_SP'),
        
        ('Ruota_DA', 'Dadi_DA'),
        ('Ruota_SA', 'Dadi_SA'),
        ('Ruota_DP', 'Dadi_DP'),
        ('Ruota_SP', 'Dadi_SP'),
        
        ('Dadi_DA', 'Copri_DA'),
        ('Dadi_SA', 'Copri_SA'),
        ('Dadi_DP', 'Copri_DP'),
        ('Dadi_SP', 'Copri_SP'),
    ]
    
    solve_with_cpmpy(duration1, max_time1, precedences)