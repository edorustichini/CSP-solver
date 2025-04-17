import time
from job_scheduling import JobShopSchedulingProblem
from solver import Solver
from main import get_cost, get_minium_cost
from CPMpy import solve_with_cpmpy

def test_three_instances():
    """
    Testa tre istanze diverse del problema JSS, con diversi max_time e durate.
    """
    # Istanza 1: Problema originale (max_time = 30)
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
    
    # Istanza 2: Vincolo temporale più stringente (max_time = 25)
    duration2 = {
        'Asse_A': 7,
        'Asse_P': 7,
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
    max_time2 = 20
    
    duration3 = {
        'Asse_A': 15,
        'Asse_P': 15,
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
        'Ispezione': 5
    }
    max_time3 = 45
    
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
    
    
    my_results = []
    cpmpy_results = []
    
    print("\n ISTANZA 1: Problema originale (max_time=30) ===")
    my_results.append(run_instance(duration1, max_time1, precedences, "Istanza 1"))
    cpmpy_results.append(solve_with_cpmpy(duration1, max_time1, precedences))
    
    '''
    print("\n ISTANZA 2: Durate e max_time ridotti")
    my_results.append(run_instance(duration2, max_time2, precedences, "Istanza 2"))
    cpmpy_results.append(solve_with_cpmpy(duration2, max_time2, precedences))

    
    

    print("\n=== ISTANZA 3: Durate e max_time aumentati1")
    my_results.append(run_instance(duration3, max_time3, precedences, "Istanza 3"))
    cpmpy_results.append(solve_with_cpmpy(duration3, max_time3, precedences))
    '''
    
    return compare(my_results, cpmpy_results)


def run_instance(duration, max_time, precedences, istance_name):
    """
    Run a single istance of the jss problem
    """

    print(f"\n--- {istance_name}: Test con il mio solver (max_time={max_time}) ---")
    
    #create problema
    operations = list(duration.keys())
    jss_problem = JobShopSchedulingProblem(operations, max_time, duration)
    
    for before, after in precedences:
        jss_problem.add_precedence_constraint(before, after)
    
    #
    jss_problem.add_disjunction_constraint('Asse_A', 'Asse_P')
    
    # "Ispezione" as final operation
    for op in operations:
        if op != 'Ispezione':
            jss_problem.add_precedence_constraint(op, 'Ispezione')
    
    # Solve the problem
    solver = Solver(jss_problem)
    start_time = time.time()
    solutions = solver.get_all_solutions()
    my_execution_time = time.time() - start_time
    
    if solutions:
        min_solutions = get_minium_cost(jss_problem, solutions)
        min_cost = get_cost(jss_problem, min_solutions[0])
        print(f"\n" + 20*"--" + "My solver" + 20*"--")
        print(f"Found  {len(solutions)} solutions")
        print(f"Found {len(min_solutions)} minimal cost soluitions ")
        print(f"Minimal cost: {min_cost}")
        print(f"Execution time: {my_execution_time:.3f} seconds")
        
        '''
        print("\n*** Minimum cost solution ***")
        optimal_sol = min_solutions[0]
        for var in sorted(optimal_sol.keys()):
            end_time = optimal_sol[var] + duration[var]
            print(f"{var}: inizio={optimal_sol[var]}, fine={end_time}")
        '''
    else:
        print("Nessuna soluzione trovata")
        min_cost = None
    
    return {
        "solutions": len(solutions) if solutions else 0,
        "min_cost": min_cost,
        "execution_time": my_execution_time
    }

def compare(results1, results2):
    for i in range(len(results1)):
        if results1[i] != results2[i]:
            return False
    return True
if __name__ == "__main__":
    results = test_three_instances()
    
    