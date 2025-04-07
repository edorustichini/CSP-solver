import random
from job_scheduling import JobShopSchedulingProblem
from solver import Solver

def jss_problem_instance(duration : dict):
    """
    Problem described in AIMA 2021 RN  chap: 6.1.2
    """
    operations = list(duration.keys())
    
    jss_problem = JobShopSchedulingProblem(operations, 30, duration)
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
    if len(solutions) == 0:
        print("Non c'è soluzione al problema")
        solutions = []
        # TODO gestire meglio caso vuoto
    
    num = 1
    if solutions:
        while num<=5:
            print("Some solutions")
            sol = random.choice(solutions)
            print(f"\nsol {num} ------------------")
            for var,value in sol.items():
                tmp = [var2 for c in jss_problem.constraints[var] for var2 in  c.variables  if var2 != var]
                print(f"{var} = {value} , ha vincoli da verificare con :{tmp}")
            num += 1
        print(f".... other {len(solutions) - num} found")
    
    # TODO: SCEGLIERE UNA SOLUZIONE A COSTO MINIMO

def get_cost(jss_p : JobShopSchedulingProblem, solution : dict):
    # in this specified example, "Ispezione" must be the last operation
    # so you can calculate the solution "cost" adding the value taken in the solution by "Ispezione" and its duration
    return solution["Ispezione"] + jss_p.operation_duration["Ispezione"]

def get_minium_cost(jss_p : JobShopSchedulingProblem, solutions : list) -> list:
    costs = []
    for i,sol in enumerate(solutions, start=0):
        costs.append(get_cost(jss_p, sol))
    minimum = min(costs)
    min_solutions = [solutions[i] for i, sol in enumerate(solutions, start=0) if costs[i] == minimum]
    return min_solutions
def choose_sol(solutions):
    return solutions[0]

if __name__ == "__main__":
    duration1= {
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
    jss_problem_instance(duration1)