import pygame
import sys
from pygame.locals import *


# Function to start the game
def start_game():
    pygame.quit()
    from DinoGames import main
    main()


# Menu function
def show_menu():
    pygame.init()

    screen = pygame.display.set_mode((1000, 750))
    pygame.display.set_caption('Dino Game: Hands Up Beta')

    # Load background image
    background_image = pygame.image.load('assets/background.jpg')
    background_image = pygame.transform.scale(background_image, (1000, 750))

    # Load background music
    pygame.mixer.music.load('assets/Like A Dino - All Songs.mp3')
    pygame.mixer.music.set_volume(0.5)  # Set volume： 0.0 ~ 1.0
    pygame.mixer.music.play(-1)  # Play indefinitely (-1 loops infinitely)

    font_title = pygame.font.SysFont('Comic Sans MS', 80, bold=True)
    font_subtitle = pygame.font.SysFont('Comic Sans MS', 30)
    font_menu = pygame.font.SysFont('Arial', 36)
    font_press = pygame.font.SysFont('Arial', 36, bold=True)

    while True:
        screen.blit(background_image, (0, 0))  # Draw the background image

        # Centering text
        title_text = font_title.render('Dino Game: ', True, (0, 0, 0))
        subtitle_text = font_title.render('Hands Up Beta', True, (0, 0, 0))
        screen.blit(title_text, (500 - title_text.get_width() // 2, 150))
        screen.blit(subtitle_text, (500 - subtitle_text.get_width() // 2, 220))

        press_text = font_press.render('Press Enter to start game', True, (0, 0, 0))
        screen.blit(press_text, (500 - press_text.get_width() // 2, 500))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == pygame.K_RETURN:  # Detect if the "Enter" key is pressed
                    pygame.mixer.music.stop()
                    start_game()


# Main program
if __name__ == "__main__":
    show_menu()
