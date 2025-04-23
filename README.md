# Constraint Satisfaction Problem Solver
Questo progetto implementa un risolutore di CSP generico.

**Exam Assignment**
>Si scriva (in un linguaggio di programmazione a scelta) un generico solver per problemi di soddisfacimento di vincoli basato
su backtracking e MAC, capace di generare tutte le soluzioni per un problema assegnato. Si consideri quindi il problema
descritto in §6.1.2 di R&N 2021 e lo si risolva enumerando tutte le soluzioni compatibili con i vincoli e scegliendone una a
costo minimo. Si applichi il metodo ad almeno tre istanze diverse.

## Funzionalità
I vari moduli presenti nel progetto danno la possibilità di:
1. Definire problemi CSP generali, a cui si può aggiungere variabili e vincoli
2. Applicare la ricerca backtracking ed enumerare tutte le soluzioni al problema
3. Risolvere problemi di job-shop scheduling e mostrarne una a "costo minimo".
## Guida

### Prerequisiti

- Python 3.10 o superiore
- cpmpy

### Esecuzione del Codice

1. Clonare questo repository
2. Navigare nella directory del progetto
3. Installare le librerie necessarie
4. Eseguire lo script principale:

```
python csp/main.py
```

Questo risolverà l'istanza che corrisponde all'esempio del libro: viene mostrato il numero di soluzioni valide trovate e soluzioni a costo minimo, per poi mostrare una soluzione a costo minimo.
Se si vogliono risolvere le 3 istanze basta fare una chiamata alla funzione `test_three_instances`.

# Relazione progetto
Il file [Relazione Progetto.pdf](Relazione%20progetto.pdf) contiene una descrizione più approfondita del progetto.
