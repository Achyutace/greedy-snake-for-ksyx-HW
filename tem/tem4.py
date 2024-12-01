import tkinter as tk
from tkinter import messagebox

class MainMenu:
    def __init__(self, root, start_game_callback, open_settings_callback):
        '''
        parse
        '''
        self.root = root
        self.root.title("Snake Game")
        self.start_game_callback = start_game_callback
        self.open_settings_callback = open_settings_callback
        self.root.geometry("400x200")
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.frame, text="Snake Game", font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.start_button = tk.Button(self.frame, text="Start Game", command=self.start_game_callback)
        self.start_button.pack(pady=10)

        self.settings_button = tk.Button(self.frame, text="Settings", command=self.open_settings_callback)
        self.settings_button.pack(pady=10)

class GameUI:
    def __init__(self, root, game_matrix):
        self.root = tk.Toplevel(root)
        self.root.title("Snake Game")
        self.game_matrix = game_matrix

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.frame, width=400, height=400)
        self.canvas.pack()

        self.update_game_state(self.game_matrix)

    def renew_game_matrix(self, new_matrix):
        self.game_matrix = new_matrix

    def update_game_state(self, new_matrix):
        self.renew_game_matrix(new_matrix)
        game_state = self.game_matrix
        self.canvas.delete("all")

        # Draw snake
        for segment in game_state['snake']:
            x, y = segment
            self.canvas.create_rectangle(x*20, y*20, (x+1)*20, (y+1)*20, fill="green")

        x, y = game_state['snake'][0]
        self.canvas.create_rectangle(x*20, y*20, (x+1)*20, (y+1)*20, fill="black")

        # Draw apple
        x, y = game_state['apple']
        self.canvas.create_oval(x*20, y*20, (x+1)*20, (y+1)*20, fill="red")

        # Update score
        self.root.title(f"Snake Game - Score: {game_state['score']}")

    def create_game_over(self):
        self.canvas.create_text(200, 200, text="Game Over", font=("Helvetica", 24))

class Settings:
    def __init__(self, root, save_settings_callback, back_to_menu_callback):
        self.root = tk.Toplevel(root)
        self.root.title("Settings")
        self.save_settings_callback = save_settings_callback
        self.back_to_menu_callback = back_to_menu_callback
        
        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.frame, text="Settings", font=("Helvetica", 24))
        self.label.pack(pady=20)

        self.animation_var = tk.BooleanVar(value=True)
        self.animation_check = tk.Checkbutton(self.frame, text="Show Real-time Animation", variable=self.animation_var)
        self.animation_check.pack(pady=10)

        self.volume_var = tk.DoubleVar(value=50.0)
        self.volume_scale = tk.Scale(self.frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", variable=self.volume_var)
        self.volume_scale.pack(pady=10)

        self.save_button = tk.Button(self.frame, text="Save Settings", command=self._save_settings_callback)
        self.save_button.pack(pady=10)

        self.back_button = tk.Button(self.frame, text="Back to Menu", command=self._back_to_menu_callback)
        self.back_button.pack(pady=10)

    def _save_settings_callback(self):
        settings = {
            'show_animation': self.animation_var.get(),
            'volume': self.volume_var.get()
        }
        self.save_settings_callback(settings)
        messagebox.showinfo("Settings", "Settings saved successfully!")

    def _back_to_menu_callback(self):
        settings_back_to_menu(self)
        

def start_game():
    game_matrix = {
        'snake': [(5, 5), (5, 6), (5, 7)],
        'apple': (10, 10),
        'score': 3,
        'game_over': False
    }
    game_ui = GameUI(root, game_matrix)

def open_settings():
    settings = Settings(root, save_settings, settings_back_to_menu)
    return settings

def save_settings(settings):

    print("Settings saved:", settings)

def settings_back_to_menu(settings):
    settings.root.destroy()
    

root = tk.Tk()
main_menu = MainMenu(root, start_game, open_settings)
root.mainloop()