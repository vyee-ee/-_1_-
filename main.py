from tkinter import *
import time
import random
import pygame

# Initialize the pygame mixer for playing sounds
pygame.mixer.init()

# Load the sound for block breaking
block_break_sound = None
try:
    block_break_sound = pygame.mixer.Sound('clash-royale-laugh.mp3')  # Replace with your actual block break sound file path
    background_music = pygame.mixer.Sound('C418_-_Subwoofer_Lullaby_30921632.mp3')  # Replace with your actual background music file path
    background_music.set_volume(0.5)
except pygame.error as e:
    print(f"Error loading sound: {e}")

class Ball:
    def __init__(self, canvas, platform, blocks, color):
        self.canvas = canvas
        self.platform = platform
        self.blocks = blocks
        self.oval = canvas.create_oval(200, 200, 215, 215, fill=color)
        self.dir = [-3, -2, -1, 1, 2, 3]
        self.x = random.choice(self.dir)
        self.y = -1
        self.touch_bottom = False

    def touch_platform(self, ball_pos):
        platform_pos = self.canvas.coords(self.platform.rect)
        if ball_pos[2] >= platform_pos[0] and ball_pos[0] <= platform_pos[2]:
            if ball_pos[3] >= platform_pos[1] and ball_pos[3] <= platform_pos[3]:
                return True
        return False

    def touch_block(self, ball_pos):
        for block in self.blocks:
            block_pos = self.canvas.coords(block.rect)
            if ball_pos[2] >= block_pos[0] and ball_pos[0] <= block_pos[2]:
                if ball_pos[1] <= block_pos[3] and ball_pos[3] >= block_pos[1]:
                    self.canvas.delete(block.rect)
                    self.blocks.remove(block)

                    # Play the block break sound
                    if block_break_sound:
                        block_break_sound.play()

                    return True
        return False

    def draw(self):
        self.canvas.move(self.oval, self.x, self.y)
        pos = self.canvas.coords(self.oval)
        if pos[1] <= 0:
            self.y = 3
        if pos[3] >= 400:
            self.touch_bottom = True
        if self.touch_platform(pos):
            self.y = -3
        if self.touch_block(pos):
            self.y *= -1
        if pos[0] <= 0:
            self.x = 3
        if pos[2] >= 500:
            self.x = -3

class Platform:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(230, 300, 330, 310, fill=color)
        self.x = 0
        self.canvas.bind_all('<KeyPress-Left>', self.left)
        self.canvas.bind_all('<KeyRelease-Left>', self.stop)
        self.canvas.bind_all('<KeyPress-Right>', self.right)
        self.canvas.bind_all('<KeyRelease-Right>', self.stop)

    def left(self, event):
        self.x = -4  # Doubled the speed from -2 to -4

    def right(self, event):
        self.x = 4  # Doubled the speed from 2 to 4

    def stop(self, event):
        self.x = 0

    def draw(self):
        self.canvas.move(self.rect, self.x, 0)
        pos = self.canvas.coords(self.rect)
        if pos[0] <= 0:
            self.x = 0
        if pos[2] >= 500:
            self.x = 0

class Block:
    def __init__(self, canvas, x1, y1, x2, y2, color):
        self.canvas = canvas
        self.rect = canvas.create_rectangle(x1, y1, x2, y2, fill=color)

def create_blocks(canvas, colors):
    blocks = []
    y_offset = 50
    for i in range(5):  # Create 5 rows of blocks
        for j in range(10):  # Each row has 10 blocks
            blocks.append(Block(canvas, j*50, y_offset, j*50+45, y_offset+20, random.choice(colors)))
        y_offset += 25
    return blocks

def play_music():
    try:
        background_music.play(-1)  # Play the music indefinitely
    except pygame.error as e:
        print(f"Error playing music: {e}")

# Initialize main window
window = Tk()
window.title("Arkanoid")
window.resizable(0, 0)
window.wm_attributes("-topmost", 1)

canvas = Canvas(window, width=500, height=400)
canvas.pack()

colors = ['red', 'orange', 'yellow', 'green', 'blue', 'purple']
blocks = create_blocks(canvas, colors)

platform = Platform(canvas, 'green')
ball = Ball(canvas, platform, blocks, 'red')

play_music()  # Start playing music

while True:
    if not ball.touch_bottom:
        ball.draw()
        platform.draw()
    else:
        break

    if not blocks:  # If all blocks are broken, end the game
        break

    window.update()
    time.sleep(0.01)

window.mainloop()

pygame.mixer.music.stop()  # Stop the music when the game ends
