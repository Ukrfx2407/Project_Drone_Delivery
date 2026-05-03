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
        self.title(f"Simulazione Istanza {numero_istanza}")
        self.geometry("1000x1000")
        self.attributes("-topmost", True)

        # CONFIGURAZIONE E DATI 
        
        self.livello_batteria = 1.0  # Partiamo dal 100% (1.0)
        self.consumo_per_mossa = 0.05 # Ogni mossa consuma il 5% (0.05)
        self.lato_cella = 160
        self.step_corrente = 0
        self.piano_pddl = []
        
        # Il tuo Dizionario GPS (Coordinate centrali delle celle)
        self.coordinate_celle = {
            "p00": (80, 80),   "p01": (240, 80),  "p02": (400, 80),  "p03": (560, 80),  "p04": (720, 80),
            "p10": (80, 240),  "p11": (240, 240), "p12": (400, 240), "p13": (560, 240), "p14": (720, 240),
            "p20": (80, 400),  "p21": (240, 400), "p22": (400, 400), "p23": (560, 400), "p24": (720, 400),
            "p30": (80, 560),  "p31": (240, 560), "p32": (400, 560), "p33": (560, 560), "p34": (720, 560),
            "p40": (80, 720),  "p41": (240, 720), "p42": (400, 720), "p43": (560, 720), "p44": (720, 720)
        }

        # --- ZONA 2: PREPARAZIONE GRAFICA ---
        self.canvas = tk.Canvas(self, width=800, height=800, bg="white", highlightthickness=0)
        self.canvas.pack(pady=20)
        
        img_pil = Image.open("house.png").resize((100, 100))
        self.img_tk_house = ImageTk.PhotoImage(img_pil)
        
        img_pil = Image.open("restaurant.png").resize((100, 100))
        self.img_tk_restaurant = ImageTk.PhotoImage(img_pil)
        self.id_house = self.canvas.create_image(720, 720, image=self.img_tk_house, tags="house")
        self.id_restaurant = self.canvas.create_image(80, 80, image=self.img_tk_restaurant, tags="restaurant")

        self.disegna_griglia()
        
        if numero_istanza == 1 : 
             img_pil = Image.open("house.png").resize((100, 100))
             self.img_tk_house = ImageTk.PhotoImage(img_pil)
             self.id_house = self.canvas.create_image(720, 720, image=self.img_tk_house, tags="house")
        if numero_istanza == 2 or numero_istanza == 3 :
            self.id_house = self.canvas.create_image(80, 720, image=self.img_tk_house, tags="house")
            self.id_house = self.canvas.create_image(720, 80, image=self.img_tk_house, tags="house")
            self.id_house = self.canvas.create_image(720, 720, image=self.img_tk_house, tags="house")
        
        # Carichiamo il drone (assicurati che il file si chiami drone.png)
        img_pil = Image.open("drone.png").resize((100, 100))
        self.img_tk = ImageTk.PhotoImage(img_pil)        
        
        self.id_drone = self.canvas.create_image(80, 80, image=self.img_tk, tags="drone")
        

        # Bottone per avviare tutto
        self.btn_start = ctk.CTkButton(self, text="Avvia Missione PDDL", command=lambda: self.avvia_missione(numero_istanza), width=200, height=40, font=("Segoe UI Variable", 16))
        self.btn_start.pack(pady=10)

        # Barra di stato per la batteria
        self.barra_batteria = ctk.CTkProgressBar(self, width=400, height=40, progress_color="#2ecc71") # Colore verde
        self.barra_batteria.pack(pady=10)
        self.barra_batteria.set(self.livello_batteria)

   
    # --- METODI GRAFICI ---
    def disegna_griglia(self):
        for i in range(1, 5):
            pos = i * self.lato_cella
            self.canvas.create_line(pos, 0, pos, 800, fill="gray", dash=(4, 4))
            self.canvas.create_line(0, pos, 800, pos, fill="gray", dash=(4, 4))


    # --- ZONA 4: IL PILOTA (MOVIMENTO FLUIDO) ---
    def muovi_verso(self, tx, ty):
        coords = self.canvas.coords("drone")
        cx, cy = coords[0], coords[1]
        passo = 5
        dx = dy = 0

        if abs(tx - cx) > 0:
            dx = tx - cx if abs(tx - cx) <= passo else (passo if tx > cx else -passo)
        if abs(ty - cy) > 0:
            dy = ty - cy if abs(ty - cy) <= passo else (passo if ty > cy else -passo)

        if dx != 0 or dy != 0:
            self.canvas.move("drone", dx, dy)
            self.after(20, lambda: self.muovi_verso(tx, ty))
        else:
            # Arrivato! Passiamo alla prossima riga del PDDL
            self.step_corrente += 1
            self.esegui_prossima_mossa()
 

    # --- ZONA 3: IL CERVELLO PDDL (LETTURA DA FILE TXT) ---
    def avvia_missione(self, numero_istanza):
        """Legge il piano dal file di testo e avvia il drone"""
        self.btn_start.configure(state="disabled") 
        
        with open(f"piano_istanza{numero_istanza}.txt", "r") as file:
            testo_planner = file.read()
        
        self.piano_pddl = self.estrai_piano_universale(testo_planner)
        self.step_corrente = 0
        
        if self.piano_pddl:
            self.esegui_prossima_mossa()
        else:
            print("❌ Il file è stato letto, ma non ho trovato azioni valide.")
            self.btn_start.configure(state="normal")
        

    def estrai_piano_universale(self, testo):
        piano = []
        for riga in testo.split("\n"):
            if "(" in riga and ")" in riga:
                azione = riga[riga.find("(")+1 : riga.find(")")].split()
                piano.append(azione)
        return piano

    def esegui_prossima_mossa(self):
        """Controlla il copione: se ci sono mosse, le lancia"""
        if self.step_corrente < len(self.piano_pddl):
            azione = self.piano_pddl[self.step_corrente]
            
            if azione[0] == "move":
                # --- SCARICA LA BATTERIA ---
                self.livello_batteria -= self.consumo_per_mossa
                self.barra_batteria.set(self.livello_batteria)
                
                # Se la batteria scende sotto il 30%, diventa rossa (emergenza)
                if self.livello_batteria < 0.3:
                    self.barra_batteria.configure(progress_color="#e74c3c")
                
                # --- MOVIMENTO ---
                dest = azione[3] 
                target_x, target_y = self.coordinate_celle[dest]
                self.muovi_verso(target_x, target_y)
            elif azione[0] == "recharge":
                print("⚡ Ricarica in corso...")
                
                # --- RIPRISTINA LA BATTERIA ---
                self.livello_batteria = 1.0
                self.barra_batteria.set(self.livello_batteria)
                self.barra_batteria.configure(progress_color="#2ecc71") # Torna verde
                
                # IMPORTANTISSIMO: Passiamo alla mossa successiva!
                self.step_corrente += 1
                
                # Pausa lunga (1.5 secondi) per simulare il tempo di ricarica e poi riparte
                self.after(1500, self.esegui_prossima_mossa)
                
            else:
                # Per load e delivery passa al comando successivo
                self.step_corrente += 1
                self.after(500, self.esegui_prossima_mossa)
        else:
            self.fine = ctk.CTkLabel(self, text="Ordine è stato consegnato", font=("Segoe UI Variable", 24, "bold"))
            self.fine.pack(pady=20)

# =========================================================
#  IL MENU PRINCIPALE (DASHBOARD)
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