from constraint import BinaryConstraint
from problem import Problem
from solver import Solver


# TODO: leggi paper (folder IA) di jobshop scheduling

def main():
    # 1. Creazione del problema
    print("Creazione problema CSP di colorazione mappa...")
    variables = ['A', 'B', 'C']
    domains = {
        'A': ['Rosso', 'Verde'],
        'B': ['Rosso', 'Verde'],
        'C': ['Rosso', 'Verde']
    }
    problem = Problem(variables, domains)
    
    # 2. Aggiunta vincoli
    print("Aggiunta vincoli...")
    constraint_AB = BinaryConstraint(('A', 'B'), lambda a, b: a != b)
    constraint_BC = BinaryConstraint(('B', 'C'), lambda b, c: b != c)
    
    problem.add_constraint(constraint_AB)
    problem.add_constraint(constraint_BC)
    
    # 3. Risoluzione
    print("Risoluzione con backtracking + MAC...")
    solver = Solver(problem)
    solutions = solver.backtracking_search()
    
    # 4. Visualizzazione risultati
    print("\nSoluzioni trovate:", len(solutions))
    for i, sol in enumerate(solutions, 1):
        print(f"\nSoluzione {i}:")
        for var, val in sorted(sol.items()):
            print(f"{var}: {val}")
    
    print("\nFine!")


if __name__ == "__main__":
    main()