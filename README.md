**Assignment:** Si scriva (in un linguaggio di programmazione a scelta) un generico solver per problemi di sodisfacimento di vincoli basato
su backtracking e MAC, capace di generare tutte le soluzioni per un problema assegnato. Si consideri quindi il problema
descritto in §6.1.2 di R&N 2021 e lo si risolva enumerando tutte le soluzioni compatibili con i vincoli e scegliendone una a
costo minimo. Si applichi il metodo ad almeno tre istanze diverse.

# Constraint Satisfaction Problem Solver
Questo progetto implementa un risolutore di CSP generico; l'implementazione è specificamente applicata a problemi di job-shop scheduling, ed è basata sulle spiegazioni presenti nel libro "Artificial Intelligence: A Modern Approach" di Russell & Norvig (2021).
## Funzionalità
I vari moduli presenti nel progetto danno la possibilità di:
1. Definire problemi CSP generali
2. Applicare la ricerca backtracking ed enumerare tutte le soluzioni al problema
3. Risolvere problemi di job-shop scheduling con vincoli di precedenza e disgiunzione, e selezionare quella a "costo minimo".
4. In aggiunta è fornito anche un semplice esempio per la colorazione della mappa dell'Australia

## Struttura dei File
- `constraint.py`: Definisce la classe base `Constraint` e la sottoclasse `BinaryConstraint` per rappresentare vincoli binari tra variabili
- `problem.py`: Implementa la classe `Problem` per rappresentare problemi CSP definendo: variabili, domini delle variabili, e vincoli tra le variabili
- `solver.py`: Contiene la classe `Solver` che implementa l'algoritmo di ricerca backtracking con MAC (Maintaining Arc Consistency)
- `job_scheduling.py`: Implementa la classe `JobShopSchedulingProblem` che estende `Problem` per modellare specificamente problemi di job scheduling
- `main.py`: Il file di esecuzione principale che crea e risolve tre diverse istanze di problemi di job scheduling
- `simple_map_colouring.py`: Un'implementazione di esempio del problema della colorazione della mappa dell'Australia (solo a scopo dimostrativo)

## Come Eseguire

### Prerequisiti

- Python 3.10 o superiore
- Nessuna libreria esterna richiesta

### Esecuzione del Codice

1. Clonare questo repository
2. Navigare nella directory del progetto
3. Eseguire lo script principale:

```
python csp/main.py
```

Questo risolverà tre diverse istanze di job scheduling, stamperà tutte le soluzioni compatibili e selezionerà la soluzione a costo minimo per ciascuna.

Se invece si vuole creare e risolvere un problema specifico si devo:
1. istanziare il problema creando un oggetto Problem
2. Aggiungere variabili, domini e vincoli al problema
3. istanziare un risolutore creando un oggetto Solver
4. Chiamare la funzione get_all_solutions del solver

### Output Atteso

Il programma:
1. Inizializzerà ogni istanza del problema
2. Applicherà AC-3 per ridurre i domini delle variabili
3. Eseguirà la ricerca backtracking per trovare tutte le soluzioni
4. Stamperà diverse soluzioni di esempio
5. Visualizzerà la soluzione a costo minimo basata sul tempo di completamento

## Descrizione di un job-shop scheduling problem

Il problema di job-shop scheduling mira a pianificare un insieme di operazioni con durate e vincoli specifici.

In questo tipo di problemi vengono usati principalmente due tipi di vincoli:

1. **Vincoli di precedenza**: L'operazione A deve essere completata prima che l'operazione B possa iniziare
2. **Vincoli di disgiunzione**: Due operazioni non possono sovrapporsi nel tempo (non possono essere eseguite simultaneamente)

Ogni variabile rappresenta un'operazione, e il valore che assume sarà il minuto in cui inizierà a eseguire il suo compito; l'obbiettivo è assegnare un tempo di inizio a ciascuna operazione rispettando tutti i vincoli.

L'esempio da ricreare era l'assemblaggio di un'automobile, le operazioni includono l'installazione di assi, ruote, dadi e coprimozzo, con specifiche relazioni di precedenza che devono essere seguite.

## Funzione di Costo

Per i problemi di job scheduling, il costo di una soluzione è definito come il tempo di completamento dell'intero lavoro (il tempo di fine massimo tra tutte le operazioni). Il solutore trova tutte le soluzioni valide e poi identifica quella con il tempo di completamento minimo.