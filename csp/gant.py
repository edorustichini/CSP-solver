import matplotlib.pyplot as plt

def create_gant(solution, durations):

    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Aggiunge ogni attività al grafico
    for i, (var, start) in enumerate(solution.items()):
        ax.barh(y=i, width=durations[var], left=start, height=0.4, align='center')
    
    # Imposta le etichette sull'asse Y
    ax.set_yticks(range(len(solution)))
    ax.set_yticklabels(solution.keys())
    
    # Etichette degli assi
    ax.set_xlabel('Tempo')
    ax.set_title('Diagramma di Gantt')
    
    # Aggiunge griglia verticale
    ax.grid(True, axis='x', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('diagramma_gantt.png', dpi=300)
