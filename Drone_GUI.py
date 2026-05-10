import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk

# Finestra di simulazione
class FinestraSimulazione(ctk.CTkToplevel):
    def __init__(self, master, numero_istanza):
        super().__init__(master)
        self.title(f"Simulazione Istanza {numero_istanza}")
        self.state("zoomed")
        self.attributes("-topmost", True)
        self.drone2_attivo = numero_istanza == 5

        # Configurazione stato iniziale
        if numero_istanza == 5:
            self.livello_batteria_drone1 = 1.0
            self.livello_batteria_drone2 = 0.4
        else:
            self.livello_batteria_drone1 = 1.0
            self.livello_batteria_drone2 = 1.0
        
        self.consumo_per_mossa = 0.05
        self.num_order_drone1 = 0
        self.num_order_drone2 = 0
        self.lato_cella = 160
        self.step_corrente = 0
        self.id_drone2 = None
        self.label_batteria_drone2 = None
        self.barra_batteria_drone2 = None
        self.label_ordini_drone2 = None
        self.label_stato = None
        self._status_reset_job = None
        
        # Setup interfaccia grafica
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

        # Caricamento immagini
        img_pil = Image.open("drone1.png").resize((100, 100))
        self.img_drone = ImageTk.PhotoImage(img_pil) 

        img_pil = Image.open("drone2.png").resize((100, 100))
        self.img_drone2 = ImageTk.PhotoImage(img_pil) 

        img_pil = Image.open("electric-station.png").resize((100, 100))
        self.img_recharge = ImageTk.PhotoImage(img_pil)
        
        img_pil = Image.open("house.png").resize((100, 100))
        self.img_house = ImageTk.PhotoImage(img_pil)
        
        img_pil = Image.open("restaurant.png").resize((100, 100))
        self.img_restaurant = ImageTk.PhotoImage(img_pil)

        self.id_restaurant = self.canvas.create_image(80, 80, image=self.img_restaurant, tags="restaurant")

        self.disegna_griglia()
        self.disegna_ostacoli(numero_istanza)

        # Posizionamento case e stazioni in base all'istanza
        case_per_istanza = {
            1: [(1040, 720)],
            2: [(80, 720), (1040, 80), (1040, 720)],
            3: [(80, 720), (1040, 80), (1040, 720)],
            4: [(80, 720), (1040, 80), (1040, 720), (560, 560)],
            5: [(880, 560), (80, 720), (1040, 80), (1040, 720), (560, 560), (720, 240)]
        }
        
        stazioni_per_istanza = {
            2: [(400, 720)],
            3: [(400, 720)],
            4: [(400, 720)],
            5: [(400, 720), (1040, 400)]
        }

        if numero_istanza in case_per_istanza:
            for x, y in case_per_istanza[numero_istanza]:
                self.canvas.create_image(x, y, image=self.img_house, tags="house")
                
        if numero_istanza in stazioni_per_istanza:
            for x, y in stazioni_per_istanza[numero_istanza]:
                self.canvas.create_image(x, y, image=self.img_recharge, tags="recharge")


        # Configurazione controlli
        self.btn_start = ctk.CTkButton(self.pannello_sinistro, text="Avvia Missione PDDL", command=lambda: self.avvia_missione(numero_istanza), width=200, height=40, font=("Segoe UI Variable", 16))
        self.btn_start.pack(pady=(10, 30))

        self.label_log = ctk.CTkLabel(self.pannello_sinistro, text="Event Log PDDL", font=("Segoe UI Variable", 18, "bold"))
        self.label_log.pack(anchor="w", padx=10, pady=(0, 8))
        self.log_eventi = ctk.CTkTextbox(self.pannello_sinistro, width=280, height=620, wrap="word")
        self.log_eventi.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        self.log_eventi.insert("end", "Log pronto.\n")
        self.log_eventi.configure(state="disabled")
        
        # Posizionamento del drone1(di default) e dei suoi indicatori
        self.id_drone1 = self.canvas.create_image(80, 80, image=self.img_drone, tags="drone1")

        self.label_batteria_drone1 = ctk.CTkLabel(self.pannello_destro, text="Batteria Drone 1", font=("Segoe UI Variable", 16, "bold"))
        self.label_batteria_drone1.pack(anchor="w", padx=10, pady=(20, 5))
        self.barra_batteria_drone1 = ctk.CTkProgressBar(self.pannello_destro, width=220, height=40, progress_color="#2ecc71")
        self.barra_batteria_drone1.pack(padx=10, pady=(0, 20))
        self.barra_batteria_drone1.set(self.livello_batteria_drone1)

        self.label_ordini_drone1 = ctk.CTkLabel(self.pannello_destro, text=f"Ordini Drone 1: {self.num_order_drone1}", font=("Segoe UI Variable", 16, "bold"))
        self.label_ordini_drone1.pack(anchor="w", padx=10, pady=(0, 10))

        # Posizionamento del drone2(solo se serve) e dei suoi indicatori
        if self.drone2_attivo:
            self.id_drone2 = self.canvas.create_image(80, 80, image=self.img_drone2, tags="drone2")
            
            self.label_batteria_drone2 = ctk.CTkLabel(self.pannello_destro, text="Batteria Drone 2", font=("Segoe UI Variable", 16, "bold"))
            self.label_batteria_drone2.pack(anchor="w", padx=10, pady=(25, 5))
            self.barra_batteria_drone2 = ctk.CTkProgressBar(self.pannello_destro, width=220, height=40, progress_color="#2ecc71")
            self.barra_batteria_drone2.pack(padx=10, pady=(0, 20))
            self.barra_batteria_drone2.set(self.livello_batteria_drone2)

            self.label_ordini_drone2 = ctk.CTkLabel(self.pannello_destro, text=f"Ordini Drone 2: {self.num_order_drone2}", font=("Segoe UI Variable", 16, "bold"))
            self.label_ordini_drone2.pack(anchor="w", padx=10, pady=(0, 10))

        self.label_stato = ctk.CTkLabel(
            self.pannello_destro,
            text="Stato: in attesa",
            font=("Segoe UI Variable", 16, "bold"),
            text_color="white",
            fg_color="#34495e",
            corner_radius=12,
            width=260,
            height=42,
        )
        self.label_stato.pack(fill="x", padx=10, pady=(20, 10))

       

       

       

        self.log_evento(f"Istanza {numero_istanza} pronta.")

    # Metodi di utility
    def coord_da_nome(self, nome_cella):
        riga = int(nome_cella[1])
        colonna = int(nome_cella[2])
        return (80 + colonna * self.lato_cella, 80 + riga * self.lato_cella)

    def disegna_griglia(self):
        for i in range(1, 7):
            pos = i * self.lato_cella
            self.canvas.create_line(pos, 0, pos, 800, fill="gray", dash=(4, 4))
            
        for i in range(1, 5):
            pos = i * self.lato_cella
            self.canvas.create_line(0, pos, 1120, pos, fill="gray", dash=(4, 4))

    def disegna_ostacoli(self, numero_istanza):
        if numero_istanza >= 4:
            ostacoli = ["p20", "p21", "p30", "p31"]
            for o in ostacoli:
                cx, cy = self.coord_da_nome(o)
                self.canvas.create_rectangle(cx-80, cy-80, cx+80, cy+80, fill="#d31601", outline="#972b0f")
                self.canvas.create_text(cx, cy, text="NO-FLY\nZONE", fill="white", font=("Arial", 12, "bold"))

    def log_evento(self, testo):
        """
        Aggiunge un messaggio al log degli eventi dell'interfaccia, 
        scorrendo automaticamente per mostrare l'ultimo inserimento.
        """
        self.log_eventi.configure(state="normal")
        self.log_eventi.insert("end", testo + "\n")
        self.log_eventi.see("end")
        self.log_eventi.configure(state="disabled")

    def aggiorna_ordini(self):
        self.label_ordini_drone1.configure(text=f"Ordini Drone 1: {self.num_order_drone1}")
        if self.label_ordini_drone2 is not None:
            self.label_ordini_drone2.configure(text=f"Ordini Drone 2: {self.num_order_drone2}")

    def aggiorna_stato(self, testo, colore="#34495e", durata=1500, auto_reset=True):
        self.label_stato.configure(text=f"{testo}", fg_color=colore)

        if self._status_reset_job is not None:
            self.after_cancel(self._status_reset_job)
            self._status_reset_job = None

        if not auto_reset:
            return

        def ripristina_stato():
            self.label_stato.configure(text="Stato: in attesa", fg_color="#34495e")
            self._status_reset_job = None

        self._status_reset_job = self.after(durata, ripristina_stato)

    # Animazione drone
    def muovi_verso(self, drone_tag, tx, ty):
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
            self.step_corrente += 1
            self.esegui_prossima_mossa()
 
    # Parsing ed esecuzione PDDL
    def avvia_missione(self, numero_istanza):
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
        if self.step_corrente < len(self.piano_pddl):
            azione = self.piano_pddl[self.step_corrente]
            testo_azione = " ".join(azione)
            drone_tag = "drone2" if "drone2" in azione else "drone1"

            if drone_tag == "drone2" and not self.drone2_attivo:
                self.log_evento(f"[warning] Azione ignorata: {testo_azione} (Drone 2 non attivo in questa istanza)")
                self.step_corrente += 1
                self.after(400, self.esegui_prossima_mossa)
                return
            
            if azione[0] == "move":
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
                self.aggiorna_stato(f"{drone_tag} in movimento", "#2980b9", auto_reset=False)

                target_x, target_y = self.coord_da_nome(dest)
                self.muovi_verso(drone_tag, target_x, target_y)
                
            elif azione[0] == "recharge":
                
                if drone_tag == "drone2":
                    self.livello_batteria_drone2 = 1.0
                    self.barra_batteria_drone2.set(self.livello_batteria_drone2)
                    self.barra_batteria_drone2.configure(progress_color="#2ecc71")
                else:
                    self.livello_batteria_drone1 = 1.0
                    self.barra_batteria_drone1.set(self.livello_batteria_drone1)
                    self.barra_batteria_drone1.configure(progress_color="#2ecc71")

                self.log_evento(f"[{drone_tag}] {testo_azione} -> batteria ricaricata")
                self.aggiorna_stato(f"{drone_tag} in ricarica", "#27ae60", 1500)
                self.step_corrente += 1
                self.after(1500, self.esegui_prossima_mossa)
                
            elif azione[0] == "load-order":
                if drone_tag == "drone2":
                    self.num_order_drone2 += 1
                else:
                    self.num_order_drone1 += 1
                self.aggiorna_ordini()
                self.log_evento(f"[{drone_tag}] {testo_azione} -> carico ordine")
                self.aggiorna_stato(f"{drone_tag} carico ordine", "#8e44ad", 1200)
                
                self.step_corrente += 1
                self.after(1200, self.esegui_prossima_mossa)
                
            elif azione[0] == "delivery-order":
                if drone_tag == "drone2":
                    self.num_order_drone2 -= 1
                else:
                    self.num_order_drone1 -= 1
                self.aggiorna_ordini()
                self.log_evento(f"[{drone_tag}] {testo_azione} -> consegna ordine")
                self.aggiorna_stato(f"{drone_tag} consegna ordine", "#d35400", 1200)
                
                self.step_corrente += 1
                self.after(1200, self.esegui_prossima_mossa)
            
            else:
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
                fg_color="#2ecc71",
                corner_radius=15,
                width=400,
                height=60
            )
            self.fine.place(relx=0.5, rely=0.5, anchor="center")

# Menu Principale (Dashboard)
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Drone Control GUI - Menu Principale")
        self.state("zoomed")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.titolo = ctk.CTkLabel(self, text="Seleziona l'Istanza da simulare", font=("Segoe UI Variable", 24, "bold"))
        self.titolo.pack(pady=40)

        for i in range(1, 6):
            btn = ctk.CTkButton(self, text=f"Apri Istanza {i}", width=200, height=40, font=("Segoe UI Variable", 16),
                                command=lambda num=i: self.apri_simulazione(num))
            btn.pack(pady=10)

    def apri_simulazione(self, numero_istanza):
        finestra = FinestraSimulazione(self, numero_istanza)

if __name__ == "__main__":
    app = App()
    app.mainloop()