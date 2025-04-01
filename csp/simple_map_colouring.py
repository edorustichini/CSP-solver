from constraint import BinaryConstraint
from problem import Problem
from solver import Solver


def main():
    # 1. Creazione del problema
    print("Creazione problema CSP di colorazione mappa...")
    
    domains = {
        'WA': ['Rosso', 'Verde', 'Blu'],
        'NT': ['Rosso', 'Verde', 'Blu'],
        'Q': ['Rosso', 'Verde', 'Blu'],
        'NSW': ['Rosso', 'Verde', 'Blu'],
        'V': ['Rosso', 'Verde', 'Blu'],
        'SA': ['Rosso', 'Verde', 'Blu'],
    }
    variables = list(domains.keys())
    problem = Problem(variables, domains)
    
    # 2. Aggiunta vincoli
    print("Aggiunta vincoli...")
    constraint_SA_WA = BinaryConstraint(('SA', 'WA'), lambda a, b: a != b)
    constraint_SA_NT = BinaryConstraint(('SA', 'NT'), lambda a, b: a != b)
    constraint_SA_Q = BinaryConstraint(('SA', 'Q'), lambda a, b: a != b)
    constraint_SA_NSW = BinaryConstraint(('SA', 'NSW'), lambda a, b: a != b)
    constraint_SA_V = BinaryConstraint(('SA', 'V'), lambda a, b: a != b)
    constraint_WA_NT = BinaryConstraint(('WA', 'NT'), lambda a, b: a != b)
    constraint_NT_Q = BinaryConstraint(('NT', 'Q'), lambda a, b: a != b)
    constraint_Q_NSW = BinaryConstraint(('Q', 'NSW'), lambda a, b: a != b)
    constraint_NSW_V = BinaryConstraint(('NSW', 'V'), lambda a, b: a != b)
    
    problem.add_constraint(constraint_SA_WA)
    problem.add_constraint(constraint_SA_NT)
    problem.add_constraint(constraint_SA_Q)
    problem.add_constraint(constraint_SA_NSW)
    problem.add_constraint(constraint_SA_V)
    problem.add_constraint(constraint_WA_NT)
    problem.add_constraint(constraint_NT_Q)
    problem.add_constraint(constraint_Q_NSW)
    problem.add_constraint(constraint_NSW_V)
    
    
    print("Risoluzione con backtracking + MAC...")
    solver = Solver(problem)
    solutions = solver.backtracking_search()
    
    #  Solutions
    print("\nSoluzioni trovate:", len(solutions))
    for i, sol in enumerate(solutions, 1):
        print(f"\nSoluzione {i}:")
        for var, val in sorted(sol.items()):
            print(f"{var}: {val}")
    

    