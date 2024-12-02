import random
import unittest

'''
游戏主逻辑
'''
class SnakeGame:
    def __init__(self, width, height):
        '''
        SnakeGame维护着一个参数矩阵
        初始化游戏矩阵
        '''
        self.width = width
        self.height = height
        self.initialize()
        
    def initialize(self):
        self.snake = [(self.width // 2, self.height // 2), (self.width // 2, (self.height // 2) - 1)]
        self.direction = (0, 1)
        self.apple = self.generate_apple()
        self.score = 0
        self.game_over = False

    def generate_apple(self):
        # generate apple randomly
        while True:
            apple = (random.randint(0, self.width - 1), random.randint(0, self.height - 1))
            if apple not in self.snake:
                return apple

    def opp_move(self,direction=None):
        # 判断是不是反方向移动
        if len(self.snake) == 1:
            return False
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
        _bd = self.snake[1]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])
        if new_head[0] == _bd[0] and new_head[1] == _bd[1]:
            return True
        else:
            return False
    def move(self, direction=None):
        if self.opp_move(direction):
            _opp_flag = True
        else:
            _opp_flag = False
        # move for a step
        
        if direction:
            if direction == 'U':
                self.direction = (0, -1)
            elif direction == 'D':
                self.direction = (0, 1)
            elif direction == 'L':
                self.direction = (-1, 0)
            elif direction == 'R':
                self.direction = (1, 0)
        if (_opp_flag) and direction:
            self.direction = (-self.direction[0], -self.direction[1])
        head = self.snake[0]
        new_head = (head[0] + self.direction[0], head[1] + self.direction[1])

        if (new_head in self.snake or
                new_head[0] < 0 or new_head[0] >= self.width or
                new_head[1] < 0 or new_head[1] >= self.height):
            self.game_over = True
            return

        self.snake.insert(0, new_head)
        self.pointplus = False
        if new_head == self.apple:
            self.score += 1
            self.pointplus = True
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
    

class TestSnakeGame(unittest.TestCase):
    '''
    测试函数
    '''
    def setUp(self):
        self.game = SnakeGame(20, 20)

    def test_initial_state(self):
        initial_state = self.game.get_game_state()
        self.assertEqual(len(initial_state['snake']), 1)
        self.assertEqual(initial_state['score'], 0)
        self.assertFalse(initial_state['game_over'])

    def test_generate_apple(self):
        apple = self.game.generate_apple()
        self.assertNotIn(apple, self.game.snake)
        self.assertTrue(0 <= apple[0] < self.game.width)
        self.assertTrue(0 <= apple[1] < self.game.height)

    def test_move_snake(self):
        initial_head = self.game.snake[0]
        self.game.move('D')
        new_head = self.game.snake[0]
        self.assertEqual(new_head, (initial_head[0], initial_head[1] + 1))

    def test_eat_apple(self):
        initial_score = self.game.score
        self.game.apple = (self.game.snake[0][0], self.game.snake[0][1] + 1)
        self.game.move('D')
        self.assertEqual(self.game.score, initial_score + 1)
        self.assertNotEqual(self.game.apple, (self.game.snake[0][0], self.game.snake[0][1] + 1))

    def test_game_over(self):
        self.game.snake = [(0, 0), (1, 0), (2, 0), (3,0)]
        self.game.move('D')
        print(self.game.snake)
        self.assertFalse(self.game.game_over)
        self.game.move('D')
        self.game.move('L')
        print(self.game.snake)
        self.assertTrue(self.game.game_over)

if __name__ == "__main__":
    unittest.main()