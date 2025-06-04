import pygame
import sys
import random
import time
import os

# Receive extracted folder path from the main executable
if len(sys.argv) > 1:
    base_path = sys.argv[1]  # Passed by the EXE
else:
    base_path = os.path.abspath(os.path.dirname(__file__))  # Default for testing

def fileExist(path):
    return os.path.exists(path)

def get_resource_path(relative_path):
    """Ensures resources are accessed correctly."""
    return os.path.join(base_path, relative_path)

def fileSearch(fileName):
    """Search for a file in Resources or Scripts."""
    resource_file = get_resource_path(os.path.join("Scripts", fileName))
    
    if fileExist(resource_file):
        return resource_file
    
    resource_file = get_resource_path(os.path.join("Resources", fileName))
    
    if fileExist(resource_file):
        return resource_file

    print(f"Error: {fileName} not found!")
    return None

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1200, 650))

# Load icon
icon_path = fileSearch("open-book.png")
if icon_path:
    icon = pygame.image.load(icon_path)
    pygame.display.set_icon(icon)
else:
    print("Warning: Icon file missing!")

pygame.display.set_caption("Instructions")

# Load sound
sound_path = fileSearch("retro-coin-3-236679.wav")
if sound_path:
    selectSound = pygame.mixer.Sound(sound_path)
else:
    print("Warning: Sound file missing!")

# Load font
font_path = fileSearch("joystix monospace.otf")
if font_path:
    font = pygame.font.Font(font_path, 13)
else:
    font = pygame.font.SysFont("Arial", 13)  # Fallback font

text = """Welcome to PONG!

Basic Rules:

When the ball comes toward your goal, move your paddle in front of the ball to prevent your opponent from scoring a point.
If the paddle is actively moving when the ball collides with it, there's a 50% chance you'll get a power hit (with an audio cue). Power hits cause the ball to move 20% faster.
If the paddle is still when the ball collides, there's a 25% chance the ball will slow down (also with an audio cue).
The first player to reach 5 points wins the game!

Two Player Mode:
In this mode, two people play against each other. Player 1: Use **W and S keys** to move. Player 2: Use **Up and Down arrows**.

Unbeatable Mode:
In this mode, a single player plays against an AI that tracks the ball with perfect precision—**completely unbeatable**.

HAVE FUN!!!
"""

# Wrap text
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

# Render text
wrapped_lines = wrap_text(text, font, 1100)
y = 50
for line in wrapped_lines:
    text_surface = font.render(line, True, (255, 255, 0))
    screen.blit(text_surface, (50, y))
    y += font.get_height() + 10

pygame.display.flip()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if sound_path:
                selectSound.play()
                time.sleep(0.45)
            running = False

pygame.quit()