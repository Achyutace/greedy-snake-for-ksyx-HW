import tkinter as tk
from tkinter import messagebox

class MainMenu:
    '''
    设置的主菜单
    '''
    def __init__(self, root, start_game_callback, open_settings_callback):
        self.root = root
        self.root.title("Snake Game")
        self.root.geometry("400x200")
        self.start_game_callback = start_game_callback
        self.open_settings_callback = open_settings_callback

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.frame, text="Snake Game", font=("Helvetica", 24))
        self.label.pack(pady=20)
        # 开始游戏
        self.start_button = tk.Button(self.frame, text="Start Game", command=self.start_game_callback)
        self.start_button.pack(pady=10)
        # 调出设置
        self.settings_button = tk.Button(self.frame, text="Settings", command=self.open_settings_callback)
        self.settings_button.pack(pady=10)
