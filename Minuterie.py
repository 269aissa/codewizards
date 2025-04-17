import tkinter as tk
from tkinter import messagebox, PhotoImage
import winsound
import os
import sys
#import pygame
from datetime import timedelta

# Gestion des chemins de fichiers pour PyInstaller
def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class TimerApp:
    def __init__(self, master):
        self.master = master
        master.title("ECLA-Timer 🏆")
        master.geometry("500x600")
        master.configure(bg="#f0f0f0")

        # Charger les images (dossier 'resources' dans le même répertoire)
        try:
            self.label_title1 = tk.Label(master, text="Bienvenue à ECLA-Timer", font=("Arial", 16, "bold"), bg="#f0f0f0")
            self.label_title2 = tk.Label(master, text="Concours de défis-lecture 2025", font=("Arial", 16, "bold"), bg="#f0f0f0")
            self.label_title3 = tk.Label(master, text="Chouani le 13 avril", font=("Arial", 16, "bold"), bg="#f0f0f0")
            self.label_title1.pack(pady=1)
            self.label_title2.pack(pady=1)
            self.label_title3.pack(pady=1)
            self.img_podium = PhotoImage(file=resource_path("./livre.png")).subsample(3)
            #self.img_coupe = PhotoImage(file=resource_path("./coupe.png"))
        except Exception as e:
            messagebox.showerror("Erreur", f"Fichiers images manquants : {e}")
            sys.exit(1)

        # Interface
        self.label_podium = tk.Label(master, image=self.img_podium, bg="#f0f0f0")
        self.label_podium.pack(pady=10)

        self.time_left = tk.StringVar(value="00:01:00")
        self.label_timer = tk.Label(
            master, textvariable=self.time_left, font=("Arial", 48), bg="#f0f0f0"
        )
        self.label_timer.pack(pady=20)

        self.entry_time = tk.Entry(master, font=("Arial", 14), justify="center")
        self.entry_time.pack(pady=10)
        self.entry_time.insert(0, "00:01:00")

        self.button_frame = tk.Frame(master, bg="#f0f0f0")
        self.button_frame.pack(pady=20)

        self.start_button = tk.Button(
            self.button_frame, text="Démarrer", command=self.start_timer,
            bg="#2ecc71", fg="white", font=("Arial", 12), padx=20
        )
        self.start_button.pack(side=tk.LEFT, padx=10)

        self.stop_button = tk.Button(
            self.button_frame, text="Arrêter", command=self.stop_timer,
            bg="#e74c3c", fg="white", font=("Arial", 12), padx=20, state=tk.DISABLED
        )
        self.stop_button.pack(side=tk.RIGHT, padx=10)

        self.reset_button = tk.Button(
            self.button_frame, text="Reinitialiser", command=self.reset_timer,
            bg="orange", fg="white", font=("Arial", 12), padx=20, state=tk.DISABLED
        )
        self.reset_button.pack(side=tk.RIGHT, padx=10)

        # Variables
        self.is_running = False
        self.remaining_seconds = 300

    def start_timer(self):
        if not self.is_running:
            try:
                h, m, s = map(int, self.entry_time.get().split(':'))
                self.remaining_seconds = h * 3600 + m * 60 + s
                if self.remaining_seconds <= 0:
                    raise ValueError
            except:
                messagebox.showerror("Erreur", "Format invalide. Utilisez HH:MM:SS")
                return

            self.is_running = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)
            self.update_timer()
            
    
    def reset_timer(self):
        """Réinitialise le timer à la valeur par défaut"""
        self.stop_timer()  # Arrête le timer si en cours
        self.time_left.set("00:00:00")
        self.entry_time.delete(0, tk.END)
        self.entry_time.insert(0, "00:00:00")
        self.remaining_seconds = self.default_time

    def stop_timer(self):
        self.is_running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def update_timer(self):
        if self.is_running and self.remaining_seconds > 0:
            self.remaining_seconds -= 1
            time_str = str(timedelta(seconds=self.remaining_seconds))
            self.time_left.set(time_str)
            self.master.after(1000, self.update_timer)
        elif self.remaining_seconds == 0:
            self.stop_timer()
            #winsound.Beep(1000, 2000)  # Bip sonore
            self.play_alarm()
            messagebox.showinfo("Terminé", "Le temps est écoulé ! 🎉")
            
    def play_alarm(self):
        """Joue le son d'alarme"""
        try:
            sound_path = resource_path("alarm.wav")
            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
            #winsound.PlaySound(sound_path)
            
        except Exception as e:
            print(f"Erreur de lecture du son : {e}")
            # Fallback sur un bip système si le fichier est introuvable
            

            
if __name__ == "__main__":
    root = tk.Tk()
    root.iconbitmap(resource_path("ECLA-Timer.ico"))
    app = TimerApp(root)
    root.mainloop()