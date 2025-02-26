import os
import pygame
import numpy as np
from PIL import Image, ImageOps


def hex_to_rgb(hex_color):
    return tuple(int(hex_color[i:i + 2], 16) for i in (0, 2, 4))


def create_mask(image_path, mask_path, background_color):
    pygame.init()

    # Get initial screen size (75% of monitor resolution)
    info = pygame.display.Info()
    initial_width, initial_height = int(info.current_w * 0.80), int(info.current_h * 0.80)

    # Set up the resizable display
    screen = pygame.display.set_mode((initial_width, initial_height), pygame.RESIZABLE)
    pygame.display.set_caption(
        "Create Mask - Left click to draw, Right click to erase, Mouse wheel to resize brush, Ctrl+wheel to zoom, Middle click to pan, Enter to save")

    # Load the image
    original_image = pygame.image.load(image_path)
    image_width, image_height = original_image.get_size()

    # Initialize zoom and pan variables
    zoom = min(initial_width / image_width, initial_height / image_height)
    pan_x, pan_y = 0, 0

    # Create mask surface
    mask = pygame.Surface((image_width, image_height))
    mask.fill(background_color)

    drawing = False
    erasing = False
    panning = False
    last_pan_pos = None
    brush_size = 50

    clock = pygame.time.Clock()

    def draw_image():
        # Calculate the scaled image size
        scaled_width = int(image_width * zoom)
        scaled_height = int(image_height * zoom)

        # Scale the image and mask
        scaled_image = pygame.transform.smoothscale(original_image, (scaled_width, scaled_height))
        scaled_mask = pygame.transform.smoothscale(mask, (scaled_width, scaled_height))

        # Calculate position to center the image
        pos_x = (screen.get_width() - scaled_width) // 2 + pan_x
        pos_y = (screen.get_height() - scaled_height) // 2 + pan_y

        # Draw the image and mask
        screen.fill((128, 128, 128))  # Fill with gray to show image bounds
        screen.blit(scaled_image, (pos_x, pos_y))
        screen.blit(scaled_mask, (pos_x, pos_y), special_flags=pygame.BLEND_RGBA_MULT)

    def screen_to_image(x, y):
        # Convert screen coordinates to image coordinates
        scaled_width = image_width * zoom
        scaled_height = image_height * zoom
        offset_x = (screen.get_width() - scaled_width) / 2 + pan_x
        offset_y = (screen.get_height() - scaled_height) / 2 + pan_y
        image_x = (x - offset_x) / zoom
        image_y = (y - offset_y) / zoom
        return image_x, image_y

    def image_to_screen(x, y):
        # Convert image coordinates to screen coordinates
        scaled_width = image_width * zoom
        scaled_height = image_height * zoom
        offset_x = (screen.get_width() - scaled_width) / 2 + pan_x
        offset_y = (screen.get_height() - scaled_height) / 2 + pan_y
        screen_x = x * zoom + offset_x
        screen_y = y * zoom + offset_y
        return screen_x, screen_y

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Window has been resized, update the display
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    drawing = True
                elif event.button == 3:  # Right mouse button
                    erasing = True
                elif event.button == 2:  # Middle mouse button
                    panning = True
                    last_pan_pos = event.pos
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # Left mouse button
                    drawing = False
                elif event.button == 3:  # Right mouse button
                    erasing = False
                elif event.button == 2:  # Middle mouse button
                    panning = False
                    last_pan_pos = None
            elif event.type == pygame.MOUSEMOTION:
                if panning and last_pan_pos:
                    dx, dy = event.pos[0] - last_pan_pos[0], event.pos[1] - last_pan_pos[1]
                    pan_x += dx
                    pan_y += dy
                    last_pan_pos = event.pos
            elif event.type == pygame.MOUSEWHEEL:
                if pygame.key.get_mods() & pygame.KMOD_CTRL:
                    # Zoom in/out
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    image_x, image_y = screen_to_image(mouse_x, mouse_y)

                    old_zoom = zoom
                    zoom = max(0.1, min(5, zoom * (1.1 ** event.y)))

                    # Adjust pan to zoom towards mouse position
                    new_mouse_x, new_mouse_y = image_to_screen(image_x, image_y)
                    pan_x += mouse_x - new_mouse_x
                    pan_y += mouse_y - new_mouse_y
                else:
                    # Adjust brush size
                    brush_size = max(1, min(120, brush_size + (event.y * 2)))
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False  # Exit loop to save

        if drawing or erasing:
            # Calculate the position on the original image
            mouse_x, mouse_y = pygame.mouse.get_pos()
            image_x, image_y = screen_to_image(mouse_x, mouse_y)

            if 0 <= image_x < image_width and 0 <= image_y < image_height:
                color = (255, 255, 255) if drawing else background_color
                pygame.draw.circle(mask, color, (int(image_x), int(image_y)), max(1, int(brush_size / zoom)))

        draw_image()

        # Draw brush outline
        mouse_pos = pygame.mouse.get_pos()
        image_x, image_y = screen_to_image(mouse_pos[0], mouse_pos[1])
        screen_x, screen_y = image_to_screen(image_x, image_y)
        pygame.draw.circle(screen, (255, 0, 0), (int(screen_x), int(screen_y)), max(1, int(brush_size)), 1)

        pygame.display.flip()
        clock.tick(60)

    # Save the mask
    pygame.image.save(mask, mask_path)


    pygame.quit()
   # change_color(mask_path)


def change_color(path):
    # img = Image.open(path)
    # img = img.convert('RGB')
    #
    # d = img.getdata()
    #
    # new_img=[]
    #
    # for itm in d:
    #     if itm[0] in list(range(76, 78)):
    #         new_img.append((0, 0, 0))
    #
    #     else:
    #         new_img.append(img)
    # img.putdata(new_img)
    # img.save('new_mask.png')
    img = Image.open(path)
    pixels=list(img.getdata())

    new_color=(0,0,0)
    modif_pixel=[new_color if pixel != (255, 255, 255) else pixel for pixel in pixels]

    modif_img = Image.new('RGB', img.size)
    modif_img.putdata(modif_pixel)

    mask_image = ImageOps.invert(modif_img)
    mask_image.save(path)





def process_images(input_dir, mask_dir, background_color):
    if not os.path.exists(mask_dir):
        os.makedirs(mask_dir)

    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.png'):
            image_path = os.path.join(input_dir, filename)
            mask_path = os.path.join(mask_dir, filename)
            create_mask(image_path, mask_path, background_color)
            print(f"Processed mask for {filename}")
            change_color(mask_path)


def check_directories(input_dir, mask_dir):
    if os.path.abspath(input_dir) == os.path.abspath(mask_dir):
        print("WARNING: The input directory and mask directory are the same.")
        print("This may result in overwriting your original images.")
        response = input("Are you sure you want to continue? Type 'Y' in uppercase to proceed: ")
        if response != 'Y':
            print("Operation cancelled. Exiting the script.")
            return False
    return True


# Example usage
input_directory = '.'  # Current directory
mask_directory = 'mask'  # Directory for masks
background_color_hex = '4D4D4D'  # Background/Unmasked color (you can change this to any hex color)
background_color_rgb = hex_to_rgb(background_color_hex)

# Check if it's safe to proceed
if check_directories(input_directory, mask_directory):
    process_images(input_directory, mask_directory, background_color_rgb)

else:
    print("Script execution terminated.")