# Simulazione PDDL: Drone Delivery

Questo repository contiene l'interfaccia grafica (GUI) e i file di simulazione per il progetto di Pianificazione Automatica (PDDL) sulla consegna di ordini tramite droni intelligenti. 
L'interfaccia permette di visualizzare in tempo reale l'esecuzione dei piani ottimali calcolati dal risolutore ENHSP per 5 diverse istanze.

## Come avviare la simulazione
Non è necessario inserire comandi manuali nel terminale. Scarica il repository (cliccando su *Code* -> *Download ZIP* ed estraendo la cartella) e segui le istruzioni per il tuo sistema operativo:

### Per utenti Windows:
1. Entra nella cartella del progetto.
2. Fai doppio clic sul file **`AVVIA_SIMULATORE.bat`**.
3. Il programma installerà automaticamente le librerie necessarie e avvierà l'interfaccia grafica.

### Per utenti Mac:
1. Apri il Terminale del Mac.
2. Trascina la cartella del progetto appena scaricata dentro la finestra del Terminale (per indicare al Mac il percorso corretto) e premi Invio.
3. Digita il seguente comando e premi Invio:
   **`sh AVVIA_MAC.command`**
4. Il programma installerà le dipendenze e si aprirà la simulazione.

*(Nota tecnica: il progetto richiede Python 3 installato sul sistema e utilizza le librerie `customtkinter` e `pillow` che vengono installate in automatico dagli script di avvio).*
