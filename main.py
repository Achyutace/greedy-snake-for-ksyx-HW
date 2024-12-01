import time
import tkinter as tk
import keyboard
from tkinter import messagebox
from serial import Serial


from frontend import *
from backend.python.utils import *
from backend.python.logic import SnakeGame

HARDMODE = 0    # 硬件模式
WIDTH = 25
HEIGHT = 25

if HARDMODE == 1:
    port = "COM5"
    ser = Serial(port, 115200, timeout=0)

else:
    ser = None

class SnakeGameApp:
    def __init__(self, root):
        self.root = root
        self.game = SnakeGame(WIDTH, HEIGHT)
        self.show_main_menu()
        self.game_started = False  # 添加一个标志来跟踪游戏是否开始
        self.last_direction = 'R'
        self.game_ui = None
        self.settings_ui = None
        self.settings_config = {
            'animation': True,
            'volume': 0
        }
        self.hardmode = HARDMODE

    def show_main_menu(self):
        # 显示主菜单
        self.main_menu = MainMenu(self.root, self.start_game, self.open_settings)

    def start_game(self):
        # 点击start_game后，调用此函数，开始游戏
        self.game_started = True  # 设置游戏开始标志
        self.game.initialize()
        self.game_ui = GameUI(game=self.game, root=self.root, ser=ser, hm = self.hardmode)
        

    def open_settings(self):
        self.settings_ui = Settings(self.root, self.save_settings, self.settings_back_to_menu, setting_args=self.settings_config)

    def save_settings(self):
        # save settings
        
        # 串口通信
        '''
        收到B，切换音量
        '''
        if(HARDMODE == 1):
            if (self.settings_ui.volume_var.get() > 50 
                and self.settings_config['volume'] < 50) or (
                    self.settings_ui.volume_var.get() < 50 
                and self.settings_config['volume'] > 50):
                ser.write("B")
        self.settings_config = {
            'animation': self.settings_ui.animation_var.get(),
            'volume': self.settings_ui.volume_var.get()
        }
        
        
        messagebox.showinfo("Settings", "Settings saved successfully!")

    def settings_back_to_menu(self):
        self.settings_ui.root.destroy()
    
    def get_game_state(self):
        direction = keyboard_process_joystick_input()
        self.game.move(direction)
        return self.game.get_game_state()


    def read_serial(self):
        c = ser.read()
        if c in ["NO", "U", "D", "L", "R"]:
            if c in ["U", "D", "L", "R"] and self.game_started:
                self.game.direction == c
        else:
            print("ERROR! STRING \"",c, "\" is read.")
        pass




root = tk.Tk()
app = SnakeGameApp(root)
if HARDMODE == 1:
    app.read_serial()
root.mainloop()