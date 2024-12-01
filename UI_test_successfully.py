import time
import tkinter as tk
import keyboard
from tkinter import messagebox
from serial import Serial


from frontend import *
from backend.python.utils import *
from backend.python.logic import SnakeGame

class SnakeGameApp:
    def __init__(self, root):
        self.root = root
        self.game = SnakeGame(20, 20)
        self.show_main_menu()
        self.game_started = False  # 添加一个标志来跟踪游戏是否开始
        self.last_direction = 'R'
        self.game_ui = None
        self.settings_ui = None
        self.settings_config = {
            'volume': 0
        }

    def show_main_menu(self):
        # 显示主菜单
        self.main_menu = MainMenu(self.root, self.start_game, self.open_settings)

    def start_game(self):
        # 点击start_game后，调用此函数，开始游戏
        self.game_started = True  # 设置游戏开始标志
        self.game_ui = GameUI(game=self.game, root=self.root)
        

    def open_settings(self):
        self.settings_ui = Settings(self.root, self.save_settings, self.settings_back_to_menu, setting_args=self.settings_config)

    def save_settings(self):
        # save settings
        
        self.settings_config = {
            'show_animation': self.settings_ui.animation_var.get(),
            'volume': self.settings_ui.volume_var.get()
        }
        # self.settings_ui.volume = _v
        messagebox.showinfo("Settings", "Settings saved successfully!")

    def settings_back_to_menu(self):
        self.settings_ui.root.destroy()
    
    def get_game_state(self):
        direction = keyboard_process_joystick_input()
        self.game.move(direction)
        return self.game.get_game_state()

    def game_loop(self):
        pass






root = tk.Tk()
app = SnakeGameApp(root)

root.mainloop()