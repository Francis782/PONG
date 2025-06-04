import pygame
import pygame
import sys
import random
import subprocess
import time
icon = pygame.image.load("open-book.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Instructions")


pygame.init()

selectSound = pygame.mixer.Sound("retro-coin-3-236679.wav") 


def wrap_text(text, font, max_width):
    lines = []
    paragraphs = text.split("\n")

    for paragraph in paragraphs:
        words = paragraph.split()
        if not words:
            lines.append("")
            continue

        current_line = words[0]
        for word in words[1:]:
            if font.size(current_line + ' ' + word)[0] <= max_width:
                current_line += ' ' + word
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
    
    return lines

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1200, 650))
font = pygame.font.Font("joystix monospace.otf", 13)
text = """Welcome to PONG!

Basic Rules:

When the ball comes toward your goal move your paddle in front of the ball to prevent your opponent from scoring a point.
If the paddle is actively moving when the ball collides with the paddle there is a 50% chance that you'll get a power hit (with an audio queue), power hits cause the ball to move 20% faster. 
If the paddle is still when the ball collides with it there is a 25% chance that the ball will slow down (also with an audio queue).
The first player to reach 5 points wins the game!

Two Player Mode:
In this game mode, two people get to play against each other. (As player 1) Use the W and S keys to move the paddle up and down respectively. (As player 2) Use the Up arrow and Down arrow keys to move the paddle up and down respectively.

Unbeatable Mode:
In this game mode, a single person plays against a computer player. This player constantly tracks the movement of the ball with perfect precision, making this player completely unbeatable.

HAVE FUN!!!
"""

# Wrap the text
wrapped_lines = wrap_text(text, font, 1100)

# Render and display the text
y = 50
for line in wrapped_lines:
    text_surface = font.render(line, True, (255, 255, 0))
    screen.blit(text_surface, (50, y))
    y += font.get_height() + 10

pygame.display.flip()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            selectSound.play()
            time.sleep(0.45)
            running = False


pygame.quit()
