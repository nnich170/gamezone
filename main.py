import tkinter as tk
from tkinter import messagebox
import subprocess
import os
import sys

def open_game(game_name):
    """Function to open the game script based on user selection."""
    game_scripts = {
        "Snake": "snake.py",
        "Car Racing": "car_racing.py",
        "Ping Pong": "pingpong.py"
    }
    
    script = game_scripts.get(game_name)
    
    if script and os.path.exists(script):
        try:
            subprocess.run([sys.executable, script], check=True)  
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
    else:
        messagebox.showerror("Error", f"Game '{game_name}' script not found!")

def create_main_menu():
    """Create the main menu with buttons for each game."""
    root = tk.Tk()
    root.title("Game Selection Menu")

    window_width = 700
    window_height = 600
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (window_width // 2)
    y = (screen_height // 2) - (window_height // 2)
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    root.resizable(False, False)
    
    root.configure(bg="#FFD700")  
    
    try:
        logo = tk.PhotoImage(file="gamezone.png")  
        logo = logo.subsample(3, 3)  
        logo_label = tk.Label(root, image=logo, bg="#FFD700")
        logo_label.image = logo 
        logo_label.pack(pady=10)
    except Exception:
        logo_label = tk.Label(root, text="Game Logo", font=("Arial", 16, "bold"), bg="#FFD700", fg="#333333")
        logo_label.pack(pady=10)
    
    label = tk.Label(root, text="Select a Game", font=("Arial", 24), bg="#FFD700", fg="black")
    label.pack(pady=10)
    
    button_style = {
        "font": ("Arial", 14),
        "bg": "#FFA500", 
        "fg": "black",    
        "activebackground": "#FF8C00",  
        "activeforeground": "black",
        "width": 20,
        "height": 2,
        "relief": "raised"
}

    button_snake = tk.Button(root, text="Snake", command=lambda: open_game("Snake"), **button_style)
    button_snake.pack(pady=10)

    button_car_racing = tk.Button(root, text="Car Racing", command=lambda: open_game("Car Racing"), **button_style)
    button_car_racing.pack(pady=10)

    button_pingpong = tk.Button(root, text="Ping Pong", command=lambda: open_game("Ping Pong"), **button_style)
    button_pingpong.pack(pady=10)
    
    footer = tk.Label(root, text="Have fun playing!", font=("Arial", 12), bg="#FFD700", fg="black")
    footer.pack(side="bottom", pady=10)
    
    root.mainloop()

if __name__ == "__main__":
    create_main_menu()
