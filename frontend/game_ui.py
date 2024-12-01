import tkinter as tk

DIFFICUTIES = 1
DELAY = int(1000/DIFFICUTIES)
'''
贪吃蛇游戏的UI界面
'''
class GameUI:
    def __init__(self, game, root, ser, hm):
        '''
        parse root: tk的主元件
        parse game: SnakeGame类维护对局的逻辑和数据
        example:
        'snake': [(5, 5), (5, 6), (5, 7)],
        'apple': (10, 10),
        'score': 3,
        'game_over': False

        '''
        self.root = tk.Toplevel(root)
        self.root.title("Snake Game")
        self.game = game
        self.ser = ser
        self.hardmode = hm
        


        self.frame = tk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.root, width=20 * game.width, height=20 * game.height)
        self.canvas.pack()

        self.root.bind("<Key>", self.on_key_press)
        self.root.focus_set()  # 确保窗口获得焦点

        self.update_game_state()


    def on_key_press(self, event):
        # 测试键盘
        key = event.keysym
        
        if key in ['Up', 'Down', 'Left', 'Right']:
            _d = {'Up': 'U', 'Down': 'D', 'Left': 'L', 'Right': 'R'}[key]
            if not self.game.opp_move(_d):
                self.game.direction = _d
            else:
                pass
            

    def update_game_state(self):
        # renew UI, 同时进行与串口的通信
        # print(self.game.direction)
        self.game.move(self.game.direction)
        game_state = self.game.get_game_state()
        self.canvas.delete("all")
        # 串口通信
        
        if self.game.pointplus and self.hardmode == 1:
            self.ser.write("A")

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

        if not game_state['game_over']:
            self.root.after(DELAY, self.update_game_state)
        else:
            self.canvas.create_text(10*self.game.width,10*self.game.height, text="Game Over", font=("Helvetica", 24))

    
    def create_game_over(self):
        self.canvas.create_text(200, 200, text="Game Over", font=("Helvetica", 24))

    

def test_game_ui_once():
    # 创建一个模拟的游戏状态
   
    g_m =  {
        'snake': [(5, 5), (5, 6), (5, 7)],
        'apple': (10, 10),
        'score': 3,
        'game_over': False
    }

    # 创建一个Tkinter根窗口
    root = tk.Tk()
    root.geometry("400x400")

    # 创建GameUI实例
    game_ui = GameUI(root, g_m)

    # 启动游戏UI
    game_ui.start_game_callback()

    # 运行Tkinter主循环
    root.mainloop()

if __name__ == "__main__":
    test_game_ui_once()