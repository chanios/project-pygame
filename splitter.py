import cv2
import numpy as np

def extract_sprites(input_image_path, sheet_background_color, sprite_background_color, y_tolerance=10):
    # Load the input image
    image = cv2.imread(input_image_path)
    # Define the lower and upper bounds for the sprite sheet background color
    lower_sheet_background = np.array(sheet_background_color, dtype=np.uint8)
    upper_sheet_background = np.array(sheet_background_color, dtype=np.uint8)

    # Define the lower and upper bounds for each sprite's background color
    lower_sprite_background = np.array(sprite_background_color, dtype=np.uint8)
    upper_sprite_background = np.array(sprite_background_color, dtype=np.uint8)

    # Create masks for the sprite sheet background and each sprite's background
    sheet_background_mask = cv2.inRange(image, lower_sheet_background, upper_sheet_background)
    sprite_background_mask = cv2.inRange(image, lower_sprite_background, upper_sprite_background)
    # Find contours in the sprite sheet background mask
    contours, _ = cv2.findContours(sprite_background_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    # Set the background pixels to transparent
    # image = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(sprite_background_mask))
    b, g, r = cv2.split(image)
    rgba = [b,g,r, cv2.bitwise_not(sprite_background_mask)]
    image = cv2.merge(rgba,4)
    # Create a directory to save the output images
    import os
    output_directory = 'output_images'
    os.makedirs(output_directory, exist_ok=True)

    # Extract and group sprites by y-coordinate with tolerance
    sprites = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        sprite = image[y:y + h, x:x + w]
        sprites.append((x, y, sprite))

    # Sort and group sprites by y-coordinate with tolerance
    sorted_sprites = []
    for x, y, sprite in sorted(sprites, key=lambda s: s[1]):
        if not sorted_sprites or (
            sorted_sprites[-1] and (
                abs(sorted_sprites[-1][-1][1] - y) > y_tolerance or
                abs(len(sorted_sprites[-1][-1][2][0]) - len(sprite[0])) > 10 or 
                abs(sorted_sprites[-1][-1][0] - (x + len(sprite[0]))) > 10
                )
            ):
            sorted_sprites.append([(x, y, sprite)])
        else:
            sorted_sprites[-1].append((x, y, sprite))

    # Save sorted sprites
    for group_index, group in enumerate(sorted_sprites, start=1):
        for sprite_index, (x, y, sprite) in enumerate(reversed(group), start=1):
            output_path = f'{output_directory}/sprite_group_{group_index+17}_sprite_{sprite_index}.png'
            cv2.imwrite(output_path, sprite)

    print(f'Extracted and grouped {len(sorted_sprites)} sprite groups. Saved in "{output_directory}" directory.')


# Example usage
input_image_path = 'PC Computer - Touhou Hyouibana Antinomy of Common Flowers - Yukari Yakumo.png'
sheet_background_color = [168, 97, 50]  # BGR values for the sprite sheet background color (3261A8)
sprite_background_color = [236, 187, 147]  # BGR values for each sprite's background color (93BBEC)
extract_sprites(input_image_path, sheet_background_color, sprite_background_color)
