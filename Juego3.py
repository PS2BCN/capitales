import tkinter as tk
from tkinter import messagebox
import random
import winsound  # Librería nativa de Windows para sonidos tipo 8-bits
import threading

class JuegoNintendoGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Super Adivinanza 1000 - NES Edition")
        self.root.geometry("400x550")
        self.root.configure(bg="#000000") # Fondo negro tipo consola antigua
        
        self.numero_secreto = random.randint(1, 1000)
        self.intentos = 0
        
        # Sonido de inicio (Melodía rápida tipo Nintendo)
        self.sonar_inicio()
        self.crear_interfaz()

    def sonar_inicio(self):
        # Pequeña melodía: Frecuencia (Hz) y Duración (ms)
        def melodia():
            winsound.Beep(440, 100) # La
            winsound.Beep(660, 100) # Mi
            winsound.Beep(880, 150) # La agudo
        threading.Thread(target=melodia, daemon=True).start()

    def sonar_error(self):
        # Sonido cuando fallas el número
        threading.Thread(target=lambda: winsound.Beep(200, 150), daemon=True).start()

    def sonar_victoria(self):
        # Fanfarria de victoria clásica
        def fanfarria():
            notas = [523, 523, 523, 523, 415, 466, 523, 0, 466, 523]
            for n in [523, 659, 783, 1046]: # Arpegio ascendente
                winsound.Beep(n, 150)
        threading.Thread(target=fanfarria, daemon=True).start()

    def crear_interfaz(self):
        # Estilo Retro Pixel
        tk.Label(self.root, text="SUPER ADIVINANZA", font=("Courier", 20, "bold"), 
                 bg="#000000", fg="#ff0000").pack(pady=20)
        
        self.lbl_intentos = tk.Label(self.root, text="INTENTOS: 0", font=("Courier", 14), 
                                     bg="#000000", fg="#ffffff")
        self.lbl_intentos.pack()

        # Pantalla de historial
        self.txt_historial = tk.Text(self.root, height=10, width=30, state='disabled', 
                                     bg="#111111", fg="#00ff00", font=("Courier", 10))
        self.txt_historial.pack(pady=10)

        # Entrada
        self.entry = tk.Entry(self.root, font=("Courier", 24), justify='center', 
                               width=8, bg="#ffffff", fg="#000000")
        self.entry.pack(pady=20)
        self.entry.bind('<Return>', lambda e: self.verificar())

        # Botón
        tk.Button(self.root, text="[ START ]", command=self.verificar,
                  bg="#ff0000", fg="#ffffff", font=("Courier", 14, "bold"),
                  width=10, relief="flat").pack(pady=10)

        self.lbl_pista = tk.Label(self.root, text="ADIVINA DEL 1 AL 1000", 
                                  font=("Courier", 10), bg="#000000", fg="#ffff00")
        self.lbl_pista.pack(pady=10)

    def verificar(self):
        try:
            num = int(self.entry.get())
        except:
            return

        self.intentos += 1
        self.lbl_intentos.config(text=f"INTENTOS: {self.intentos}")

        if num < self.numero_secreto:
            self.lbl_pista.config(text=f"ES MAS GRANDE ↑")
            self.sonar_error()
        elif num > self.numero_secreto:
            self.lbl_pista.config(text=f"ES MAS PEQUEÑO ↓")
            self.sonar_error()
        else:
            self.sonar_victoria()
            messagebox.showinfo("YOU WIN", f"¡CONSEGUIDO!\nNúmero: {self.numero_secreto}")
            self.root.destroy()

        # Actualizar historial
        self.txt_historial.config(state='normal')
        self.txt_historial.insert(tk.END, f"INTENTO {self.intentos}: {num}\n")
        self.txt_historial.see(tk.END)
        self.txt_historial.config(state='disabled')
        self.entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = JuegoNintendoGUI(root)
    root.mainloop()