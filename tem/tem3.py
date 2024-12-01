import tkinter as tk
import random
import time

TIME = 45
class SnakeGame:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.snake = [(width // 2, height // 2)]
        self.direction = (0, 1)
        self.apple = self.generate_apple()
        self.score = 0
        self.game_over = False

    def generate_apple(self):
        while True:
            apple = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if apple not in self.snake:
                return apple

    def move(self, direction=None):
        if direction:
            if direction == 'U':
                self.direction = (0, -1)
            elif direction == 'D':
                self.direction = (0, 1)
            elif direction == 'L':
                self.direction = (-1, 0)
            elif direction == 'R':
                self.direction = (1, 0)
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        if (new_head in self.snake or
                new_head[0] < 0 or new_head[0] >= self.width or
                new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return

        self.snake.insert(0, new_head)

        if new_head == self.apple:
            self.score += 1
            self.apple = self.generate_apple()
        else:
            self.snake.pop()

    def get_game_state(self):
        return {
            'snake': self.snake,
            'apple': self.apple,
            'score': self.score,
            'game_over': self.game_over
        }

class GameUI:
    def __init__(self, root, game):
        self.root = root
        self.root.title("Snake Game")
        self.game = game

        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()
        
        self.root.bind("<Key>", self.on_key_press)
        self.update_game_state()

    def on_key_press(self, event):
        key = event.keysym
        
        if key in ['Up', 'Down', 'Left', 'Right']:
            self.game.direction = {'Up': 'U', 'Down': 'D', 'Left': 'L', 'Right': 'R'}[key]
            
            

    def update_game_state(self):
        self.game.move(self.game.direction)
        game_state = self.game.get_game_state()
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

        if not game_state['game_over']:
            self.root.after(TIME, self.update_game_state)
        else:
            self.canvas.create_text(200, 200, text="Game Over", font=("Helvetica", 24))

def main():
    root = tk.Tk()
    game = SnakeGame(20, 20)
    game_ui = GameUI(root, game)
    time.sleep(1)

    root.mainloop()

if __name__ == "__main__":
    
    main()