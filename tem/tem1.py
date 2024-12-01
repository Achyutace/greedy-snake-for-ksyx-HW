import time
from logic import SnakeGame
from utils import process_joystick_input, play_sound

def main():
    game = SnakeGame(20, 20)
    clock_period = 0.1  # 每个时钟周期的时间，单位为秒

    while not game.game_over:
        start_time = time.time()

        # 1. 获取硬件输入（如摇杆数据）
        direction = process_joystick_input()

        # 2. 通知逻辑层处理（如移动蛇）
        game.move(direction)

        # 3. 获取游戏状态
        game_state = game.get_game_state()

        # 4. 更新硬件状态（模拟）
        print(f"Snake: {game_state['snake']}")
        print(f"Apple: {game_state['apple']}")
        print(f"Score: {game_state['score']}")

        # 5. 播放音效（如果需要）
        if game_state['game_over']:
            play_sound('game_over.wav')

        # 6. 等待下一个时钟周期
        elapsed_time = time.time() - start_time
        if elapsed_time < clock_period:
            time.sleep(clock_period - elapsed_time)

    print("Game Over!")

if __name__ == "__main__":
    main()