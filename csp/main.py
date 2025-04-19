from gant import create_gant
from job_scheduling import JobShopSchedulingProblem
from solver import Solver
from CPMpy import solve_with_cpmpy


def get_cost(jss_p : JobShopSchedulingProblem, solution : dict):
    # in this specified example, "Ispezione" must be the last operation
    # so you can calculate the solution's "cost" adding the value taken in the solution by "Ispezione" and its duration
    return solution["Ispezione"] + jss_p.operation_duration["Ispezione"]

def get_minium_cost(problem, solutions):
    min_cost = min(get_cost(problem, sol) for sol in solutions)
    return [sol for sol in solutions if get_cost(problem, sol) == min_cost]
def choose_sol(solutions):
    return solutions[0]

def test_three_instances(precedences, duration1, max_time1, duration2, max_time2, duration_3, max_time3):
    my_results = []
    cpmpy_results = []
    
    print("\n Instance n. 1")
    my_results.append(run_instance(duration1, max_time1, precedences, "Instance 1"))
    cpmpy_results.append(solve_with_cpmpy(duration1, max_time1, precedences))
    
    
    print("\n Instance n.2")
    my_results.append(run_instance(duration2, max_time2, precedences, "Instance n.2"))
    cpmpy_results.append(solve_with_cpmpy(duration2, max_time2, precedences))
    
    
    print("\n Instance n. 3")
    cpmpy_results.append(solve_with_cpmpy(duration3, max_time3, precedences))
    my_results.append(run_instance(duration3, max_time3, precedences, "Instance n.3"))
    


def run_instance(duration, max_time, precedences, name=" "):
    """
    Run a single istance of the jss problem
    """

    print(f"\n--- {name}: My solver ---")
    
    #create problem
    operations = list(duration.keys())
    jss_problem = JobShopSchedulingProblem(operations, max_time, duration)

    
    for before, after in precedences:
        jss_problem.add_precedence_constraint(before, after)
    
    jss_problem.add_disjunction_constraint('Asse_A', 'Asse_P')
    
    for op in operations:
        if op != 'Ispezione':
            jss_problem.add_precedence_constraint(op, 'Ispezione')  # adds constraints for final operation

    # Solve the problem
    solver = Solver(jss_problem)
    solutions = solver.get_all_solutions()

    min_solutions = get_minium_cost(jss_problem, solutions)
    min_cost = get_cost(jss_problem, min_solutions[0])
    print(f"Found  {len(solutions)} solutions")
    print(f"Found {len(min_solutions)} minimal cost solutions")
    print(f"Minimal cost: {min_cost}")
    
    
    print("\n*** Minimum cost solution ***")
    optimal_sol = min_solutions[0]
    for var in sorted(optimal_sol.keys()):
        end_time = optimal_sol[var] + duration[var]
        print(f"{var}: inizio={optimal_sol[var]}, fine={end_time}")
    
    return {
        "solutions": len(solutions) if solutions else 0,
        "min_cost": min_cost,
        "opt_sol": optimal_sol
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
    
    duration2 = {
        'Asse_A': 5,
        'Asse_P': 5,
        'Ruota_DA': 2,
        'Ruota_SA': 2,
        'Ruota_DP': 2,
        'Ruota_SP': 2,
        'Dadi_DA': 1,
        'Dadi_SA': 1,
        'Dadi_DP': 1,
        'Dadi_SP': 1,
        'Copri_DA': 1,
        'Copri_SA': 1,
        'Copri_DP': 1,
        'Copri_SP': 1,
        'Ispezione': 2
    }
    max_time2 = 18
    
    duration3 = {
        'Asse_A': 12,
        'Asse_P': 12,
        'Ruota_DA': 5,
        'Ruota_SA': 5,
        'Ruota_DP': 5,
        'Ruota_SP': 5,
        'Dadi_DA': 3,
        'Dadi_SA': 3,
        'Dadi_DP': 3,
        'Dadi_SP': 3,
        'Copri_DA': 2,
        'Copri_SA': 2,
        'Copri_DP': 2,
        'Copri_SP': 2,
        'Ispezione': 4
    }
    max_time3 = 40
    
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
    #test_three_instances(precedences, duration1, max_time1, duration2, max_time2, duration3, max_time3)
    result = run_instance(duration1, max_time1, precedences)
    create_gant(result["opt_sol"], duration1)

