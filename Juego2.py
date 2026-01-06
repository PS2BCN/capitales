import tkinter as tk
from tkinter import messagebox
import random
import webbrowser
import threading
import time

# Intentar cargar winsound de forma ultra-segura
try:
    import winsound
    AUDIO = True
except:
    AUDIO = False

class JuegoGanador:
    def __init__(self, root):
        self.root = root
        self.root.title("TERMINAL HACKER - CONCURSO 2026")
        self.root.geometry("450x650")
        self.root.configure(bg="#050505")
        
        # Variables de lógica
        self.objetivo = random.randint(1, 1000)
        self.intentos = 0
        self.max_intentos = 12
        
        self.interfaz()
        self.boot_sequence()

    def boot_sequence(self):
        """Efecto de sonido de inicio"""
        if AUDIO:
            threading.Thread(target=lambda: winsound.Beep(800, 200), daemon=True).start()

    def interfaz(self):
        # Título Estilo Neón
        self.titulo = tk.Label(self.root, text="SYSTEM BREACH", font=("Courier New", 28, "bold"),
                               bg="#050505", fg="#00f3ff")
        self.titulo.pack(pady=20)

        # Botón de Música Externa
        tk.Button(self.root, text="[ CONECTAR MÚSICA BSO ]", 
                  command=lambda: webbrowser.open("https://www.youtube.com/watch?v=4xDzrJKXOOY"),
                  bg="#111", fg="#666", relief="flat", font=("Arial", 8)).pack()

        # Terminal de Logs
        self.log = tk.Text(self.root, height=12, width=40, state='disabled',
                           bg="#000", fg="#0aff00", font=("Consolas", 10),
                           borderwidth=1, relief="solid")
        self.log.pack(pady=20)

        # Zona de Input
        tk.Label(self.root, text="INTRODUCE CÓDIGO DE ACCESO:", font=("Consolas", 10),
                 bg="#050505", fg="white").pack()
        
        self.entrada = tk.Entry(self.root, font=("Consolas", 30, "bold"), justify='center',
                                bg="#111", fg="#ff00ff", insertbackground="#ff00ff",
                                width=8, relief="flat")
        self.entrada.pack(pady=10)
        
        # ARREGLO DE ERROR: Usamos una función normal en lugar de lambda directo si fallaba
        self.entrada.bind('<Return>', self.procesar_evento)
        self.entrada.focus_set()

        # Botón Ejecutar
        self.btn = tk.Button(self.root, text="EJECUTAR HACKEO", command=self.verificar,
                             bg="#ff00ff", fg="white", font=("Consolas", 12, "bold"),
                             width=20, pady=10, relief="flat", cursor="hand2")
        self.btn.pack(pady=20)

        # Barra de Estado
        self.lbl_info = tk.Label(self.root, text="ESTADO: ESPERANDO SEÑAL...", 
                                 font=("Consolas", 10), bg="#050505", fg="#555")
        self.lbl_info.pack(side="bottom", pady=10)

    def procesar_evento(self, event):
        """Maneja la tecla Enter sin errores"""
        self.verificar()

    def escribir_log(self, mensaje):
        self.log.config(state='normal')
        self.log.insert(tk.END, f"> {mensaje}\n")
        self.log.see(tk.END)
        self.log.config(state='disabled')

    def verificar(self):
        # Obtener valor
        data = self.entrada.get().strip()
        if not data.isdigit():
            return
        
        num = int(data)
        self.intentos += 1
        self.entrada.delete(0, tk.END)

        # Sonido de procesado
        if AUDIO:
            threading.Thread(target=lambda: winsound.Beep(600, 50), daemon=True).start()

        # Lógica de comparación
        if num == self.objetivo:
            self.victoria()
        elif self.intentos >= self.max_intentos:
            self.derrota()
        else:
            if num < self.objetivo:
                self.escribir_log(f"INTENTO {self.intentos}: {num} (BAJO)")
                self.lbl_info.config(text="ERROR: CÓDIGO DEMASIADO BAJO", fg="#ff2a2a")
            else:
                self.escribir_log(f"INTENTO {self.intentos}: {num} (ALTO)")
                self.lbl_info.config(text="ERROR: CÓDIGO DEMASIADO ALTO", fg="#ff2a2a")

    def victoria(self):
        if AUDIO:
            threading.Thread(target=lambda: [winsound.Beep(1000, 100), winsound.Beep(1500, 300)], daemon=True).start()
        
        self.titulo.config(text="SISTEMA HACKEADO", fg="#0aff00")
        messagebox.showinfo("¡GANASTE!", f"Acceso concedido.\nEl código era: {self.objetivo}\nIntentos: {self.intentos}")
        self.root.destroy()

    def derrota(self):
        if AUDIO:
            winsound.Beep(200, 600)
        messagebox.showerror("ALERTA", f"Cortafuegos activado. Bloqueo total.\nEl código era: {self.objetivo}")
        self.root.destroy()

if __name__ == "__main__":
    try:
        app_root = tk.Tk()
        juego = JuegoGanador(app_root)
        app_root.mainloop()
    except Exception as e:
        print(f"Error crítico: {e}")
        input("Presiona Enter para cerrar...")