from cpmpy import *

def solve_with_cpmpy(durations, max_time, precedence_constraints):
    operations = list(durations.keys())

    operations = { op: intvar(1, max_time -durations[op], name=op) for op in operations}
    
    model = Model() # collection of constraints over variables, it represents the CSP problem
    
    
    for before, after in precedence_constraints:
        model += (operations[before] + durations[before] <= operations[after])
    
        
    # Disjunction constraints
    a, b = 'Asse_A', 'Asse_P'
    model += ((operations[a] + durations[a] <= operations[b]) | (operations[b] + durations[b] <= operations[a]))

    for op in operations:
        if op != 'Ispezione':
            model += (operations[op] + durations[op] <= operations['Ispezione'])

    solutions_with_cost = []

    def collect_solution():
        cost = operations['Ispezione'].value() + durations['Ispezione']
        sol = {op: operations[op].value() for op in operations}
        solutions_with_cost.append((cost, sol))

    print("\nCPMpy is searching for solutions...")

    model.solveAll(display=collect_solution)
    
    def get_cost(sol):
        return sol['Ispezione'] + durations['Ispezione']
    
    solutions = [sol for cost, sol in solutions_with_cost]
    n_solutions = len(solutions)
    
    if n_solutions > 0:
        min_cost = min(get_cost(sol) for sol in solutions)
        min_solutions = [sol for sol in solutions if get_cost(sol) == min_cost]
        print(f"\n" + 20*"--" + "CPMpy solver" + 20*"--")
        print(f"Found {n_solutions} solutions")
        print(f"Found {len(min_solutions)} minimal cost solutions ")
        print(f"Minimal cost: {min_cost}")
    
    else:
        print("No solution to the problem")
        min_cost = None
    return {
        "solutions": len(solutions) if solutions else 0,
        "min_cost":  min_cost,
    }
    
