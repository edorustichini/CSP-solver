from cpmpy import *
import numpy as np

duration = {
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

operations = list(duration.keys())
max_time = 30

# Create variable for every operation: their values are integers
start = {
    op: intvar(1, max_time - duration[op], name=f"start_{op}") for op in operations
}

model = Model() # collection of constraints over variables, it represents the CSP problem

# Precedence constraints
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
for before, after in precedences:
    model += (start[before] + duration[before] <= start[after])

# Disjunction constraints
a, b = 'Asse_A', 'Asse_P'
model += ((start[a] + duration[a] <= start[b]) | (start[b] + duration[b] <= start[a]))

# 'Ispezione' must begin after all the others
for op in operations:
    if op != 'Ispezione':
        model += (start[op] + duration[op] <= start['Ispezione'])

def get_cost(solution):
    return solution['Ispezione'] + duration['Ispezione']


solutions = []


def print_solution():
    #TODO: capisci a cosa serve
    sol = {op: start[op].value() for op in operations}
    solutions.append(sol)


# TODO: capisci quale solver usa
n_solutions = model.solveAll(display=print_solution)

print(f"Found {n_solutions} solutions")

if n_solutions > 0:
    min_cost = min(get_cost(sol) for sol in solutions)
    min_solutions = [sol for sol in solutions if get_cost(sol) == min_cost]
    
    print("\n*** Minimum cost solution ***")
    chosen = min_solutions[0]
    for var in sorted(chosen, key=lambda x: chosen[x]):
        print(f"{var} = {chosen[var]}")
    print(f"Cost: {get_cost(chosen)}")

else:
    print("No solution to the problem")
