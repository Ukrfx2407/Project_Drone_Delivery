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
        self.state("zoomed")
        self.attributes("-topmost", True)

        # CONFIGURAZIONE E DATI 
        if numero_istanza == 5:
            self.livello_batteria_drone1 = 1.0
            self.livello_batteria_drone2 = 0.4
        else:
            self.livello_batteria_drone1 = 1.0
            self.livello_batteria_drone2 = 1.0
        
        self.consumo_per_mossa = 0.05 # Ogni mossa consuma il 5% (0.05)
        self.num_order_drone1 = 0
        self.num_order_drone2 = 0
        self.lato_cella = 160
        self.step_corrente = 0
        
        # Il tuo Dizionario GPS (Coordinate centrali delle celle)
        self.coordinate_celle = {
            
            "p00": (80, 80),   "p01": (240, 80),  "p02": (400, 80),  "p03": (560, 80),  "p04": (720, 80),  "p05": (880, 80),  "p06": (1040, 80),
            "p10": (80, 240),  "p11": (240, 240), "p12": (400, 240), "p13": (560, 240), "p14": (720, 240), "p15": (880, 240), "p16": (1040, 240),
            "p20": (80, 400),  "p21": (240, 400), "p22": (400, 400), "p23": (560, 400), "p24": (720, 400), "p25": (880, 400), "p26": (1040, 400),
            "p30": (80, 560),  "p31": (240, 560), "p32": (400, 560), "p33": (560, 560), "p34": (720, 560), "p35": (880, 560), "p36": (1040, 560),
            "p40": (80, 720),  "p41": (240, 720), "p42": (400, 720), "p43": (560, 720), "p44": (720, 720), "p45": (880, 720), "p46": (1040, 720)
        }

        # --- ZONA 2: PREPARAZIONE GRAFICA ---
        self.layout = ctk.CTkFrame(self, fg_color="transparent")
        self.layout.pack(fill="both", expand=True, padx=20, pady=20)

        self.pannello_sinistro = ctk.CTkFrame(self.layout, width=320)
        self.pannello_sinistro.pack(side="left", fill="y", padx=(0, 20))
        self.pannello_sinistro.pack_propagate(False)

        self.area_canvas = ctk.CTkFrame(self.layout, fg_color="transparent")
        self.area_canvas.pack(side="left", fill="both", expand=True)

        self.pannello_destro = ctk.CTkFrame(self.layout, width=300)
        self.pannello_destro.pack(side="right", fill="y", padx=(20, 0))
        self.pannello_destro.pack_propagate(False)

        self.canvas = tk.Canvas(self.area_canvas, width=1120, height=800, bg="#3c3c40", highlightthickness=0)
        self.canvas.pack()

        img_pil = Image.open("drone.png").resize((100, 100))
        self.img_drone = ImageTk.PhotoImage(img_pil) 

        img_pil = Image.open("electric-station.png").resize((100, 100))
        self.img_recharge = ImageTk.PhotoImage(img_pil)
        
        img_pil = Image.open("house.png").resize((100, 100))
        self.img_house = ImageTk.PhotoImage(img_pil)
        
        img_pil = Image.open("restaurant.png").resize((100, 100))
        self.img_restaurant = ImageTk.PhotoImage(img_pil)

        self.id_restaurant = self.canvas.create_image(80, 80, image=self.img_restaurant, tags="restaurant")


        self.disegna_griglia()
        self.disegna_ostacoli(numero_istanza)

        if numero_istanza == 1 : 
             self.id_house = self.canvas.create_image(1040, 720, image=self.img_house, tags="house")
        elif numero_istanza == 2 or numero_istanza == 3:
            self.id_house = self.canvas.create_image(80, 720, image=self.img_house, tags="house")
            self.id_house = self.canvas.create_image(1040, 80, image=self.img_house, tags="house")
            self.id_house = self.canvas.create_image(1040, 720, image=self.img_house, tags="house")
            self.id_recharge = self.canvas.create_image(400, 720, image=self.img_recharge, tags="recharge")
        elif numero_istanza == 4:
            self.id_house = self.canvas.create_image(80, 720, image=self.img_house, tags="house")
            self.id_house = self.canvas.create_image(1040, 80, image=self.img_house, tags="house")
            self.id_house = self.canvas.create_image(1040, 720, image=self.img_house, tags="house")
            self.id_house = self.canvas.create_image(560, 560, image=self.img_house, tags="house")
            self.id_recharge = self.canvas.create_image(400, 720, image=self.img_recharge, tags="recharge")
        elif numero_istanza == 5:
            self.id_house = self.canvas.create_image(880, 560, image=self.img_house, tags="house")
            self.id_house = self.canvas.create_image(80, 720, image=self.img_house, tags="house")
            self.id_house = self.canvas.create_image(1040, 80, image=self.img_house, tags="house")
            self.id_house = self.canvas.create_image(1040, 720, image=self.img_house, tags="house")
            self.id_house = self.canvas.create_image(560, 560, image=self.img_house, tags="house")
            self.id_house = self.canvas.create_image(720, 240, image=self.img_house, tags="house")
            self.id_recharge = self.canvas.create_image(400, 720, image=self.img_recharge, tags="recharge")
            self.id_recharge = self.canvas.create_image(1040, 400, image=self.img_recharge, tags="recharge")
            self.id_drone2 = self.canvas.create_image(80,80, image=self.img_drone, tags="drone2")

        # Carichiamo il drone (assicurati che il file si chiami drone.png)
               
        
        # Creiamo due droni (taggati separatamente) per supportare più UAV
        self.id_drone1 = self.canvas.create_image(80, 80, image=self.img_drone, tags="drone1")
        # Posizioniamo il secondo drone (stesso aspetto) in basso a destra
        
        # Bottone per avviare simulazione
        self.btn_start = ctk.CTkButton(self.pannello_sinistro, text="Avvia Missione PDDL", command=lambda: self.avvia_missione(numero_istanza), width=200, height=40, font=("Segoe UI Variable", 16))
        self.btn_start.pack(pady=(10, 30))

        self.label_log = ctk.CTkLabel(self.pannello_sinistro, text="Event Log PDDL", font=("Segoe UI Variable", 18, "bold"))
        self.label_log.pack(anchor="w", padx=10, pady=(0, 8))
        self.log_eventi = ctk.CTkTextbox(self.pannello_sinistro, width=280, height=620, wrap="word")
        self.log_eventi.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_eventi.insert("end", "Log pronto.\n")
        self.log_eventi.configure(state="disabled")

        # Barre di stato per le batterie dei due droni
        self.label_batteria_drone1 = ctk.CTkLabel(self.pannello_destro, text="Batteria Drone 1", font=("Segoe UI Variable", 16, "bold"))
        self.label_batteria_drone1.pack(anchor="w", padx=10, pady=(10, 5))
        self.barra_batteria_drone1 = ctk.CTkProgressBar(self.pannello_destro, width=220, height=40, progress_color="#2ecc71")
        self.barra_batteria_drone1.pack(padx=10, pady=(0, 20))
        self.barra_batteria_drone1.set(self.livello_batteria_drone1)

        self.label_batteria_drone2 = ctk.CTkLabel(self.pannello_destro, text="Batteria Drone 2", font=("Segoe UI Variable", 16, "bold"))
        self.label_batteria_drone2.pack(anchor="w", padx=10, pady=(0, 5))
        self.barra_batteria_drone2 = ctk.CTkProgressBar(self.pannello_destro, width=220, height=40, progress_color="#2ecc71")
        self.barra_batteria_drone2.pack(padx=10, pady=(0, 20))
        self.barra_batteria_drone2.set(self.livello_batteria_drone2)

        self.label_ordini_drone1 = ctk.CTkLabel(self.pannello_destro, text=f"Ordini Drone 1: {self.num_order_drone1}", font=("Segoe UI Variable", 16, "bold"))
        self.label_ordini_drone1.pack(anchor="w", padx=10, pady=(10, 5))

        self.label_ordini_drone2 = ctk.CTkLabel(self.pannello_destro, text=f"Ordini Drone 2: {self.num_order_drone2}", font=("Segoe UI Variable", 16, "bold"))
        self.label_ordini_drone2.pack(anchor="w", padx=10, pady=(0, 10))

        self.log_evento(f"Istanza {numero_istanza} pronta.")

       
   
    # --- METODI GRAFICI ---
    def disegna_griglia(self):
        # Disegna 6 linee VERTICALI (per separare 7 colonne)
        for i in range(1, 7):
            pos = i * self.lato_cella
            self.canvas.create_line(pos, 0, pos, 800, fill="gray", dash=(4, 4))
            
        # Disegna 4 linee ORIZZONTALI (per separare 5 righe)
        for i in range(1, 5):
            pos = i * self.lato_cella
            self.canvas.create_line(0, pos, 1120, pos, fill="gray", dash=(4, 4))

    def disegna_ostacoli(self, numero_istanza):
        # Visualizza le No-Fly Zone per le istanze 4 e 5
        if numero_istanza >= 4:
            ostacoli = ["p20", "p21", "p30", "p31"]
            for o in ostacoli:
                if o in self.coordinate_celle:
                    cx, cy = self.coordinate_celle[o]
                    # Disegna un quadrato centrato sulla cella (lato = 160)
                    self.canvas.create_rectangle(cx-80, cy-80, cx+80, cy+80, fill="#d31601", outline="#972b0f")
                    self.canvas.create_text(cx, cy, text="NO-FLY\nZONE", fill="white", font=("Arial", 12, "bold"))

    def log_evento(self, testo):
        self.log_eventi.configure(state="normal")
        self.log_eventi.insert("end", testo + "\n")
        self.log_eventi.see("end")
        self.log_eventi.configure(state="disabled")

    def aggiorna_ordini(self):
        self.label_ordini_drone1.configure(text=f"Ordini Drone 1: {self.num_order_drone1}")
        self.label_ordini_drone2.configure(text=f"Ordini Drone 2: {self.num_order_drone2}")

    def estrai_drone_azione(self, azione):
        # Scansiona tutti i token dell'azione per trovare un identificatore di drone.
        for token in azione:
            t = token.lower()
            if t in ("d1", "drone1", "drone_1", "drone-1"):
                return "drone1"
            if t in ("d2", "drone2", "drone_2", "drone-2"):
                return "drone2"
        # Nessun drone esplicitamente indicato: assumiamo drone1
        return "drone1"

    # --- ZONA 4: IL PILOTA (MOVIMENTO FLUIDO) ---
    def muovi_verso(self, drone_tag, tx, ty):
        """Sposta il drone identificato da `drone_tag` verso (tx, ty)."""
        ids = self.canvas.find_withtag(drone_tag)
        if not ids:
            return
        item_id = ids[0]
        coords = self.canvas.coords(item_id)
        if not coords:
            return
        cx, cy = coords[0], coords[1]
        passo = 5
        dx = dy = 0

        if abs(tx - cx) > 0:
            dx = tx - cx if abs(tx - cx) <= passo else (passo if tx > cx else -passo)
        if abs(ty - cy) > 0:
            dy = ty - cy if abs(ty - cy) <= passo else (passo if ty > cy else -passo)

        if dx != 0 or dy != 0:
            self.canvas.move(item_id, dx, dy)
            self.after(20, lambda: self.muovi_verso(drone_tag, tx, ty))
        else:
            # Arrivato! Passiamo alla prossima riga del PDDL
            self.step_corrente += 1
            self.esegui_prossima_mossa()
 

    # --- ZONA 3: IL CERVELLO PDDL (LETTURA DA FILE TXT) ---
    def avvia_missione(self, numero_istanza):
        """Legge il piano dal file di testo e avvia il drone"""
        self.btn_start.configure(state="disabled") 
        self.log_evento("Missione avviata.")
        
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
            testo_azione = " ".join(azione)
            
            if azione[0] == "move":
                # --- SCARICA LA BATTERIA ---
                drone_tag = self.estrai_drone_azione(azione)
                dest = azione[-1]

                if drone_tag == "drone2":
                    self.livello_batteria_drone2 -= self.consumo_per_mossa
                    self.barra_batteria_drone2.set(self.livello_batteria_drone2)
                    if self.livello_batteria_drone2 < 0.3:
                        self.barra_batteria_drone2.configure(progress_color="#e74c3c")
                else:
                    self.livello_batteria_drone1 -= self.consumo_per_mossa
                    self.barra_batteria_drone1.set(self.livello_batteria_drone1)
                    if self.livello_batteria_drone1 < 0.3:
                        self.barra_batteria_drone1.configure(progress_color="#e74c3c")

                self.log_evento(f"[{drone_tag}] {testo_azione}")

                target_x, target_y = self.coordinate_celle[dest]
                self.muovi_verso(drone_tag, target_x, target_y)
            elif azione[0] == "recharge":
                drone_tag = self.estrai_drone_azione(azione)
                
                # --- RIPRISTINA LA BATTERIA ---
                if drone_tag == "drone2":
                    self.livello_batteria_drone2 = 1.0
                    self.barra_batteria_drone2.set(self.livello_batteria_drone2)
                    self.barra_batteria_drone2.configure(progress_color="#2ecc71") # Torna verde
                else:
                    self.livello_batteria_drone1 = 1.0
                    self.barra_batteria_drone1.set(self.livello_batteria_drone1)
                    self.barra_batteria_drone1.configure(progress_color="#2ecc71") # Torna verde

                self.log_evento(f"[{drone_tag}] {testo_azione} -> batteria ricaricata")
                
                # IMPORTANTISSIMO: Passiamo alla mossa successiva!
                self.step_corrente += 1
                
                # Pausa lunga (1.5 secondi) per simulare il tempo di ricarica e poi riparte
                self.after(1500, self.esegui_prossima_mossa)
            elif azione[0] == "load-order":
                drone_tag = self.estrai_drone_azione(azione)
                if drone_tag == "drone2":
                    self.num_order_drone2 += 1
                else:
                    self.num_order_drone1 += 1
                self.aggiorna_ordini()
                self.log_evento(f"[{drone_tag}] {testo_azione} -> carico ordine")
                
                # IMPORTANTISSIMO: Passiamo alla mossa successiva!
                self.step_corrente += 1
                
                # Pausa lunga (1.5 secondi) per simulare il tempo di ricarica e poi riparte
                self.after(700, self.esegui_prossima_mossa)
            elif azione[0] == "delivery-order":
                drone_tag = self.estrai_drone_azione(azione)
                if drone_tag == "drone2":
                    self.num_order_drone2 -= 1
                else:
                    self.num_order_drone1 -= 1
                self.aggiorna_ordini()
                self.log_evento(f"[{drone_tag}] {testo_azione} -> consegna ordine")
                
                # IMPORTANTISSIMO: Passiamo alla mossa successiva!
                self.step_corrente += 1
                
                self.after(700, self.esegui_prossima_mossa)
            
            else:
                # Per load e delivery passa al comando successivo
                self.log_evento(f"[info] {testo_azione}")
                self.step_corrente += 1
                self.after(500, self.esegui_prossima_mossa)
        else:
            self.log_evento("Missione completata.")
            
            self.fine = ctk.CTkLabel(
                self, 
                text=" 🎉 Tutti gli ordini consegnati! 🚁 ", 
                font=("Segoe UI Variable", 28, "bold"),
                text_color="white",
                fg_color="#2ecc71",   # Un bel verde acceso
                corner_radius=15,     # Bordi belli arrotondati
                width=400,
                height=60
            )
           
            self.fine.place(relx=0.5, rely=0.5, anchor="center")

# =========================================================
#  IL MENU PRINCIPALE (DASHBOARD)
# =========================================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Drone Control GUI - Menu Principale")
        self.state("zoomed")
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