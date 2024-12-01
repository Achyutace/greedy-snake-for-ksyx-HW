import time
import tkinter as tk
import keyboard
from tkinter import messagebox
from serial import Serial


from frontend.main_menu import MainMenu
from frontend.settings import Settings
from frontend.game_ui import GameUI
from backend.python.logic import SnakeGame
from backend.python.utils import keyboard_process_joystick_input, process_joystick_input, play_sound

try:
    port = "COM5"
    ser = Serial(port, 115200, timeout=0)
except:
    pass

class SnakeGameApp:
    def __init__(self, root):
        self.root = root
        self.game = SnakeGame(20, 20)
        self.show_main_menu()
        self.game_started = False  # 添加一个标志来跟踪游戏是否开始
        self.last_direction = 'R'
        self.game_ui = None
        self.settings = {
            'volume': 0
        }

    def show_main_menu(self):
        # 显示主菜单
        self.main_menu = MainMenu(self.root, self.start_game, self.open_settings)

    def start_game(self):
        # 点击start_game后，调用此函数，开始游戏
        self.game_started = True  # 设置游戏开始标志
        self.game_ui = GameUI(self.root, self.get_game_state)
        # self.game_ui.start_game_callback()
        # self.game_loop()  # 开始游戏循环

    def open_settings(self):
        self.settings = Settings(self.root, self.save_settings, self.show_main_menu)

    def save_settings(self, settings):
        # settings
        self.settings = {
            # 'show_animation': self.animation_var.get(),
            'volume': settings.volume_var.get()
        }
        messagebox.showinfo("Settings", "Settings saved successfully!")

    def get_game_state(self):
        direction = keyboard_process_joystick_input()
        self.game.move(direction)
        return self.game.get_game_state()

    def game_loop(self):
        '''
        进入游戏后，开始游戏循环
        '''
        clock_period = 0.1  # 每个时钟周期的时间，单位为秒

    
        start_time = time.time()
        
        # 1. 获取键盘数据
        direction = self.last_direction
        while((time.time() - start_time)< 0.08):
            event = keyboard.read_event()
            if event.event_type == keyboard.KEY_DOWN:
                if event.name == 'w':
                    direction = 'U'  # Up
                    break
                elif event.name == 's':
                    direction = 'D'  # Down
                    break
                elif event.name == 'a':
                    direction = 'L'  # Left
                    break
                elif event.name == 'd':
                    direction = 'R'  # Right
                    break
        self.last_direction = direction
        # direction = keyboard_process_joystick_input()

        # 2. 通知logic.py处理
        self.game.move(direction)

        # 3. 更新UI
        self.game_ui.update_game_state()

        # 4. 播放音效
        # if self.game.get_game_state()['game_over']:
        #     play_sound('game_over.wav')

        # 5. 等待下一个时钟周期
        elapsed_time = time.time() - start_time
        if elapsed_time < clock_period:
            time.sleep(clock_period - elapsed_time)
        else:
            messagebox.showinfo("hhh")

        

def main():
    root = tk.Tk()
    app = SnakeGameApp(root)


if __name__ == "__main__":
    root = tk.Tk()
    app = SnakeGameApp(root)
    root.mainloop()