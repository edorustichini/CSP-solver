from constraint import BinaryConstraint
from problem import Problem
from solver import Solver


def main():
    # 1. Creazione del problema
    print("Creazione problema CSP di colorazione mappa...")
    
    domain = ['Rosso', 'Verde', 'Blu']
     #TODO: aggiungere var T (Tamzamia?) come nel libro, che è variabile senza vincoli
    problem = Problem()
    problem.add_variables_same_domain(domain, ['WA', 'NT','Q','NSW','V','SA'])
    
    print("Adding constraints...")
    #FIXME: si dovbrebbero mettere i vincoli in tutte e due i varsi
    constraints = [
        # in this problem the constraints are symmetric
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
    
    print("Vincoli:")
    for c in constraints:
        problem.add_constraint(c)
        print(f"{c.variables}")
    
    
    
    print("Risoluzione con backtracking + MAC...")
    solver = Solver(problem)
    solutions = solver.backtracking_search()
    
    #  Solutions
    print("\nSoluzioni trovate:", len(solutions))
    for i, sol in enumerate(solutions, 1):
        print(f"\nSoluzione {i}:")
        for var, val in sorted(sol.items()):
            print(f"{var}: {val}")
    
main()

    