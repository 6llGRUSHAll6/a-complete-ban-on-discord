import os
import psutil
import threading
import time
import tkinter as tk
from tkinter import messagebox


class DiscordBlockerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Discord Blocker")
        self.is_running = False

        # Интерфейс
        self.status_label = tk.Label(root, text="Статус: Отключено", fg="red", font=("Arial", 14))
        self.status_label.pack(pady=10)

        self.start_button = tk.Button(root, text="Запустить разблокировку", command=self.start_blocker, bg="green", fg="white", font=("Arial", 12))
        self.start_button.pack(pady=5)

        self.stop_button = tk.Button(root, text="Остановить разблокировку", command=self.stop_blocker, bg="red", fg="white", font=("Arial", 12))
        self.stop_button.pack(pady=5)

    def start_blocker(self):
        if not self.is_running:
            self.is_running = True
            self.status_label.config(text="Статус: Включено", fg="green")
            threading.Thread(target=self.run_blocker, daemon=True).start()
        else:
            messagebox.showinfo("Информация", "Блокировка уже запущена!")

    def stop_blocker(self):
        if self.is_running:
            self.is_running = False
            self.status_label.config(text="Статус: Отключено", fg="red")
        else:
            messagebox.showinfo("Информация", "разблокировка уже остановлена!")

    def run_blocker(self):
        """Фоновый процесс блокировки Discord."""
        while self.is_running:
            for process in psutil.process_iter(attrs=["pid", "name"]):
                try:
                    process_name = process.info["name"].lower()
                    if "discord" in process_name:
                        os.kill(process.info["pid"], 9)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            time.sleep(5)


if __name__ == "__main__":
    root = tk.Tk()
    app = DiscordBlockerApp(root)
    root.mainloop()
