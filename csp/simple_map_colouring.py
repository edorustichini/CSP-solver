from constraint import BinaryConstraint
from problem import Problem
from solver import Solver

print("Australia map colouring")

domain = ['Rosso', 'Verde', 'Blu']
problem = Problem()
problem.add_variables_same_domain(domain, ['WA', 'NT','Q','NSW','V','SA'])

print("Adding constraints...")
constraints = [ #neibouring regions must have different colors
    BinaryConstraint(('SA', 'WA'), lambda a, b: a != b),
    
    BinaryConstraint(('SA', 'NT'), lambda a, b: a != b),
    
    BinaryConstraint(('SA', 'Q'), lambda a, b: a != b),
    
    BinaryConstraint(('SA', 'NSW'), lambda a, b: a != b),
    
    BinaryConstraint(('SA', 'V'), lambda a, b: a != b),
    
    BinaryConstraint(('WA', 'NT'), lambda a, b: a != b),
    
    BinaryConstraint(('NT', 'Q'), lambda a, b: a != b),
    
    BinaryConstraint(('Q', 'NSW'), lambda a, b: a != b),
    
    BinaryConstraint(('NSW', 'V'), lambda a, b: a != b),
]

print("Adding constraints...:")
for c in constraints:
    problem.add_constraint(c)
    

print("Backtracking...")
solver = Solver(problem)
solutions = solver.backtracking_search()

#  Solutions
print(f"\nFound {len(solutions)} solutions")
for i, sol in enumerate(solutions, start=1):
    print(f"\nSol. {i}:")
    for var, val in sorted(sol.items()):
        print(f"{var}: {val}")
    
    