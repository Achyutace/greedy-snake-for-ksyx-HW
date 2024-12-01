import tkinter as tk
from tkinter import messagebox

'''
设置面板
'''
class Settings:
    def __init__(self, root, save_settings_callback, back_to_menu_callback, setting_args):
        '''
        parse save_settings_callback: func when click save settings
        parse back_to_menu_callback: func when click back_to_menu
        '''
        self.root = tk.Toplevel(root)
        self.root.title("Settings")
        self.save_settings_callback = save_settings_callback
        self.back_to_menu_callback = back_to_menu_callback
        
        self.volume = setting_args['volume']
        self.animation = setting_args['animation']

        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)                            # 整个窗口都是它的

        self.create_widgets()

    def create_widgets(self):
        # label
        self.label = tk.Label(self.frame, text="Settings", font=("Helvetica", 24))
        self.label.pack(pady=20)

        # 显示实时蛇轨迹，迭代2的主要任务
        self.animation_var = tk.BooleanVar(value=self.animation)
        self.animation_check = tk.Checkbutton(self.frame, text="Show Real-time Animation", variable=self.animation_var)
        self.animation_check.pack(pady=10)

        # 调节蜂鸣器音量
        self.volume_var = tk.DoubleVar(value=self.volume)
        self.volume_scale = tk.Scale(self.frame, from_=0, to=100, orient=tk.HORIZONTAL, label="Volume", variable=self.volume_var)
        self.volume_scale.pack(pady=10)

        # 保存设置按钮
        self.save_button = tk.Button(self.frame, text="Save Settings", command=self.save_settings_callback)
        self.save_button.pack(pady=10)

        # 关闭设置按钮
        self.back_button = tk.Button(self.frame, text="Back to Menu", command=self.back_to_menu_callback)
        self.back_button.pack(pady=10)

