import pygame
import sys
import click

@click.command()
@click.argument('image_path', type=click.Path(exists=True))
def run_viewer(image_path):
    screen_width = 700
    screnn_height = 700
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screnn_height))
    # Load the image outside the loop
    image_path = str(image_path)
    try:
        image = pygame.image.load(image_path)
    except pygame.error:
        print("Invalid input image path")
        sys.exit()
    original_image = image.copy()
    size =original_image.get_size()
    caution = size[0]/size[1]
    ratio = 1
    mx = max(size)
    if mx > screen_width: 
        ratio = screen_width / mx
    width_ratio = 1
    height_ratio = 1
    if caution > 1:
        height_ratio = 1/caution
    if caution < 1:
        width_ratio = caution
    image = pygame.transform.scale(original_image, (int(size[0] * ratio), int(size[1] * ratio)))
    image_rect = image.get_rect()
    image_rect.center = screen.get_rect().center
    clicked = False
    ctrl_pressed = False
    zoom_in = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit()
                if event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                    ctrl_pressed = True
                elif event.unicode == '+' and ctrl_pressed:
                    (width, height) = image.get_size()
                    (x, y) = image_rect.left, image_rect.top
                    image = pygame.transform.scale(original_image, (width + 70*width_ratio, height + 70*height_ratio))
                    image_rect = image.get_rect()
                    image_rect.topleft = (x, y)
                elif event.unicode == '-' and ctrl_pressed:
                    (width, height) = image.get_size()
                    image = pygame.transform.scale(original_image, (width - 70*width_ratio, height - 70*height_ratio))
                    image_rect = image.get_rect()
                    image_rect.center = screen.get_rect().center
            elif event.type == pygame.KEYUP:
                if event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                    ctrl_pressed = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if clicked == False:
                    clicked = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if clicked == True:
                    clicked = False
            elif event.type == pygame.MOUSEMOTION and clicked == True:
                image_rect.move_ip(event.rel)
                

        screen.fill((255, 255, 255))  # Clear the screen
        screen.blit(image, image_rect)
        pygame.display.flip()


run_viewer()
