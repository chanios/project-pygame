import pygame
import numpy as np
import sys

pygame.init()

WIDTH, HEIGHT = 1280, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Black Hole Distorted Effect")

# Load your image
image = pygame.image.load("as.png").convert_alpha()

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Create a numpy array from the image for faster pixel manipulation
    image_array = pygame.surfarray.array3d(image)

    # Create an array of coordinates for the X and Y positions
    x_coords, y_coords = np.meshgrid(np.arange(WIDTH), np.arange(HEIGHT))

    # Calculate distances from mouse position
    distances = np.sqrt((x_coords - mouse_x) ** 2 + (y_coords - mouse_y) ** 2)

    # Apply distortion effect
    distortion_amount = 1 / (distances * 0.01 + 1)  # You can adjust the distortion strength here
    distorted_x = (x_coords + (x_coords - mouse_x) * distortion_amount).astype(int)
    distorted_y = (y_coords + (y_coords - mouse_y) * distortion_amount).astype(int)

    # Ensure the distorted coordinates are within the image boundaries
    distorted_x = np.clip(distorted_x, 0, WIDTH - 1)
    distorted_y = np.clip(distorted_y, 0, HEIGHT - 1)

    # Apply distortion to the image array
    distorted_image_array = image_array[distorted_x, distorted_y]

    # Create a new Pygame surface from the distorted image array
    distorted_surface = pygame.surfarray.make_surface(distorted_image_array)

    screen.blit(distorted_surface, (0, 0))
    pygame.display.flip()

    clock.tick(60)