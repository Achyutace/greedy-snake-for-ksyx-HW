import pygame
import keyboard

def play_sound(sound_file):
    pygame.mixer.init()
    pygame.mixer.music.load(sound_file)
    pygame.mixer.music.play()

def process_joystick_input():
    pygame.init()
    joystick = pygame.joystick.Joystick(0)
    joystick.init()
    x_axis = joystick.get_axis(0)
    y_axis = joystick.get_axis(1)
    if abs(x_axis) > abs(y_axis):
        if x_axis > 0:
            return 'R'  # Right
        else:
            return 'L'  # Left
    else:
        if y_axis > 0:
            return 'D'  # Down
        else:
            return 'U'  # Up
        

def keyboard_process_joystick_input():
    while True:
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:
            if event.name == 'w':
                return 'U'  # Up
            elif event.name == 's':
                return 'D'  # Down
            elif event.name == 'a':
                return 'L'  # Left
            elif event.name == 'd':
                return 'R'  # Right
            
