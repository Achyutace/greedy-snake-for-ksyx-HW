import tkinter as tk

def update_ui(*args):
    # 当 my_var 发生变化时，更新 UI
    label.config(text=my_var.get())

# 创建主窗口
root = tk.Tk()
root.title("监听参数更新 UI")

# 创建一个 StringVar 变量
my_var = tk.StringVar()

# 设置初始值
my_var.set("Hello, World!")

# 监听 my_var 的变化
my_var.trace("w", update_ui)

# 创建一个标签来显示 my_var 的值
label = tk.Label(root, textvariable=my_var)
label.pack(pady=10)

# 创建一个输入框来修改 my_var 的值
entry = tk.Entry(root, textvariable=my_var)
entry.pack(pady=10)

# 运行主循环
root.mainloop()