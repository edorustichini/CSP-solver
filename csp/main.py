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
    
    print("Some solutions")
    num = 5
    for i, solution in enumerate(solutions[:num], start=1):
        print(f"Solution n. {i} :")
        for op, value in solution.items():
            print(f"{op} = {value}")
        print("------------------------------------------------------------------------- \n")
    print(f".... other {len(solutions) - 5} found")
    
    # TODO: SCEGLIERE UNA SOLUZIONE A COSTO MINIMO


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