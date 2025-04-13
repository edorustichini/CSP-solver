# Constraint Satisfaction Problem Solver
Questo progetto implementa un risolutore di CSP generico; l'implementazione è specificamente applicata a problemi di job-shop scheduling, ed è basata sulle spiegazioni presenti nel libro "Artificial Intelligence: A Modern Approach" di Russell & Norvig (2021).

**Exam Assignment**
>Si scriva (in un linguaggio di programmazione a scelta) un generico solver per problemi di sodisfacimento di vincoli basato
su backtracking e MAC, capace di generare tutte le soluzioni per un problema assegnato. Si consideri quindi il problema
descritto in §6.1.2 di R&N 2021 e lo si risolva enumerando tutte le soluzioni compatibili con i vincoli e scegliendone una a
costo minimo. Si applichi il metodo ad almeno tre istanze diverse.

## Funzionalità
I vari moduli presenti nel progetto danno la possibilità di:
1. Definire problemi CSP generali, a cui si può aggiungere variabili e vincoli
2. Applicare la ricerca backtracking ed enumerare tutte le soluzioni al problema
3. Risolvere problemi di job-shop scheduling selezionare quella a "costo minimo".
4. E' fornito un semplice esempio per la colorazione della mappa dell'Australia

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
