import os
import time
import subprocess
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

# =========================================================
# CLASSE 2: LA FINESTRA SECONDARIA (LA SIMULAZIONE)
# =========================================================
class FinestraSimulazione(ctk.CTkToplevel):
    def __init__(self, master, numero_istanza):
        super().__init__(master)
        
        # Usiamo il numero_istanza per personalizzare il titolo
        self.title(f"Simulazione Istanza {numero_istanza}")
        self.geometry("1000x1000")
        
        # Questa riga forza la nuova finestra a stare "sopra" il menu principale
        self.attributes("-topmost", True) 

        self.dizionario_celle = {}

        # Il titolo in alto nella nuova finestra
        self.titolo = ctk.CTkLabel(self, text=f"Esecuzione Piano PDDL: Istanza {numero_istanza}", font=("Segoe UI Variable", 20, "bold"))
        self.titolo.pack(pady=20)

        self.lato_cella = 160
        self.canvas = tk.Canvas(self, width=800, height=800, bg="white", highlightthickness=0)
        self.canvas.pack(expand = True)

        self.disegna_griglia()

        immagine_pil = Image.open("drone.png").resize((100, 100))
        self.immagine_tk = ImageTk.PhotoImage(immagine_pil)
        
        centro = self.lato_cella / 2  
        

        
        immagine_pil = Image.open("drone.png").resize((100, 100))
        self.immagine_tk = ImageTk.PhotoImage(immagine_pil)
        self.id_drone = self.canvas.create_image(centro, centro, image=self.immagine_tk, tags="drone")
        self.after(1000, lambda: self.muovi_drone(50, 50))
      
    
    def muovi_drone(self, x, y):
        if x < 360 and y < 360:
            self.canvas.move("drone", 5, 5)
            self.after(50, lambda: self.muovi_drone(x + 5, y + 5))

    def disegna_griglia(self):
         for i in range(1, 5):
            pos = i * self.lato_cella 
            
            # Linee verticali
            self.canvas.create_line(pos, 0, pos, 800, fill="gray", dash=(4, 4))
            # Linee orizzontali
            self.canvas.create_line(0, pos, 800, pos, fill="gray", dash=(4, 4))

    def lancia_enhsp(self, file_dominio, file_problema):
        """
        Lancia il file .jar di ENHSP in background, cattura il risultato 
        e lo passa al nostro estrattore universale.
        """
        # Assicurati che il nome del file .jar sia esattamente quello che ti ha dato il prof!
        nome_jar = "enhsp-20.jar" 
        
        # Costruiamo il comando come se lo stessimo scrivendo nel terminale
        comando = [
            "java", 
            "-jar", nome_jar, 
            "-o", file_dominio, 
            "-f", file_problema
        ]
        
        print(f"Lancio il planner per {file_problema}... attendere prego ⏳")
        
        try:
            # shell=True serve a volte su Windows per far trovare 'java'
            # capture_output=True è la magia che salva il testo invece di stamparlo
            processo = subprocess.run(comando, capture_output=True, text=True, shell=True)
            
            # Tutto il testo che ENHSP ha prodotto!
            testo_grezzo = processo.stdout
            
            # Se c'è stato un errore nel PDDL (es. errore di sintassi)
            if "Failed" in testo_grezzo or processo.returncode != 0:
                print("⚠️ Errore nel PDDL! Ecco cosa dice ENHSP:")
                print(processo.stderr or testo_grezzo)
                return []
                
            # Se ha successo, diamo in pasto il testo grezzo alla funzione di prima!
            piano_pulito = self.estrai_piano_universale(testo_grezzo)
            
            print("✅ Piano trovato e decodificato con successo!")
            return piano_pulito
            
        except FileNotFoundError:
            print("❌ ERRORE: Python non trova Java o il file enhsp.jar!")
            return []

    def leggi_pddl(self):
        print("Qui scriveremo la logica per far muovere il drone!")



# =========================================================
# CLASSE 1: IL MENU PRINCIPALE (DASHBOARD)
# =========================================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Drone Control GUI - Menu Principale")
        self.geometry("600x500")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.titolo = ctk.CTkLabel(self, text="Seleziona l'Istanza da simulare", font=("Segoe UI Variable", 24, "bold"))
        self.titolo.pack(pady=40)

        # Invece di scrivere 5 bottoni a mano, usiamo un ciclo for!
        for i in range(1, 6):
            # Creiamo i bottoni. Nota il parametro 'command' con 'lambda': 
            # serve per passare il numero corretto (1, 2, 3...) alla funzione senza eseguirla subito.
            btn = ctk.CTkButton(self, text=f"Apri Istanza {i}", width=200, height=40, font=("Segoe UI Variable", 16),
                                command=lambda num=i: self.apri_simulazione(num))
            btn.pack(pady=10)

    def apri_simulazione(self, numero_istanza):
        # Quando premi un bottone, Python "istanzia" (crea) la nuova finestra
        # passandogli il numero dell'istanza cliccata.
        finestra = FinestraSimulazione(self, numero_istanza)


if __name__ == "__main__":
    app = App()
    app.mainloop()