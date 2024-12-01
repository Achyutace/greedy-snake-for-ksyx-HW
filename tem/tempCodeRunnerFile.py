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