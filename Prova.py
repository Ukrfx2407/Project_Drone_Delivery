import os
import time
import subprocess
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
# =========================================================
# CLASSE 1: IL MENU PRINCIPALE (DASHBOARD)
# =========================================================
class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Drone Control GUI - Menu Principale")
        self.geometry("1000x1000")
        ctk.set_appearance_mode("Dark")
        ctk.set_default_color_theme("blue")

        self.canvas = tk.Canvas(self, width=800, height=800, bg="white", highlightthickness=0)
        self.canvas.pack(expand = True)
        
        self.lato_cella = 160
        
        for i in range(1, 5):
            pos = i * self.lato_cella 
            
            # Linee verticali
            self.canvas.create_line(pos, 0, pos, 800, fill="gray", dash=(4, 4))
            # Linee orizzontali
            self.canvas.create_line(0, pos, 800, pos, fill="gray", dash=(4, 4))

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

if __name__ == "__main__":
    app = App()
    app.mainloop()