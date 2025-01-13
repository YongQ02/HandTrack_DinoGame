import pygame
import random
import cv2
from mediapipe_util.mediapipe_input import detect_hand_gesture

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 300
GROUND_Y = SCREEN_HEIGHT - 100
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (83, 83, 83)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dino Run: Hands Up Beta!")
clock = pygame.time.Clock()

pygame.mixer.init()
# Load Audio
try:
    pygame.mixer.music.load('assets/Like A Dino - All Songs.mp3')
    pygame.mixer.music.set_volume(0.5)
    DEATH_SOUND = pygame.mixer.Sound('assets/gameover.mp3')
    SCORE_SOUND = pygame.mixer.Sound('assets/scoreup.mp3')
except:
    print("Warning: Some audio files could not be loaded. Continuing without sound.")


class Dino:
    def __init__(self):
        self.run_imgs = [
            pygame.transform.scale(pygame.image.load("assets/dino2.png"), (44, 47)),
            pygame.transform.scale(pygame.image.load("assets/dino2.png"), (44, 47))
        ]
        self.jump_img = pygame.transform.scale(pygame.image.load("assets/dino2.png"), (44, 47))
        self.duck_imgs = [
            pygame.transform.scale(pygame.image.load("assets/dino2.png"), (59, 30)),
            pygame.transform.scale(pygame.image.load("assets/dino2.png"), (59, 30))
        ]
        self.dead_img = pygame.transform.scale(pygame.image.load("assets/dino2.png"), (44, 47))

        self.x = 50
        self.y = GROUND_Y
        self.y_duck = GROUND_Y + 17
        self.vel_y = 0
        self.gravity = 0.8
        self.jump_speed = -16
        self.is_jumping = False
        self.is_ducking = False
        self.is_dead = False

        self.step_index = 0
        self.animation_speed = 4

        self.rect = pygame.Rect(self.x, self.y, 44, 47)
        self.duck_rect = pygame.Rect(self.x, self.y_duck, 59, 30)
        self.score_milestone = 100

    def jump(self):
        if not self.is_jumping and not self.is_dead:
            self.vel_y = self.jump_speed
            self.is_jumping = True
            self.is_ducking = False

    def duck(self):
        if not self.is_jumping and not self.is_dead:
            self.is_ducking = True

    def stop_duck(self):
        self.is_ducking = False

    def update(self):
        if self.is_jumping:
            self.y += self.vel_y
            self.vel_y += self.gravity

            if self.y >= GROUND_Y:
                self.y = GROUND_Y
                self.is_jumping = False
                self.vel_y = 0

        if self.is_ducking:
            self.rect = self.duck_rect
            self.rect.y = self.y_duck
        else:
            self.rect = pygame.Rect(self.x, self.y, 44, 47)
            self.rect.y = self.y

        if self.step_index >= self.animation_speed * 2:
            self.step_index = 0

    def draw(self):
        if self.is_dead:
            screen.blit(self.dead_img, (self.x, self.y))
            return

        if self.is_jumping:
            screen.blit(self.jump_img, (self.x, self.y))
        elif self.is_ducking:
            screen.blit(self.duck_imgs[self.step_index // self.animation_speed], (self.x, self.y_duck))
        else:
            screen.blit(self.run_imgs[self.step_index // self.animation_speed], (self.x, self.y))

        self.step_index += 1
        if self.step_index >= self.animation_speed * 2:
            self.step_index = 0


class Obstacle:
    def __init__(self, image, type):
        self.image = image
        self.type = type
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH

        if type == "cactus":
            self.rect.y = GROUND_Y + 2
        else:
            self.rect.y = GROUND_Y - 50 - random.randint(0, 30)

    def update(self, game_speed):
        self.rect.x -= game_speed

    def draw(self):
        screen.blit(self.image, self.rect)


class Cloud:
    def __init__(self):
        self.image = pygame.transform.scale(pygame.image.load("assets/cloud.jpeg"), (46, 13))
        self.x = SCREEN_WIDTH
        self.y = random.randint(50, 150)
        self.speed = 2

    def update(self):
        self.x -= self.speed

    def draw(self):
        screen.blit(self.image, (self.x, self.y))


class Ground:
    def __init__(self):
        self.y = GROUND_Y + 35
        self.dots = []

        for i in range(0, SCREEN_WIDTH, 50):
            self.dots.append({"x": i, "y": self.y + 5})

    def update(self, game_speed):
        for dot in self.dots:
            dot["x"] -= game_speed

        for dot in self.dots:
            if dot["x"] < -10:
                dot["x"] = SCREEN_WIDTH + 10

    def draw(self):
        pygame.draw.line(screen, GRAY, (0, self.y), (SCREEN_WIDTH, self.y), 2)

        for dot in self.dots:
            pygame.draw.circle(screen, GRAY, (int(dot["x"]), int(dot["y"])), 2)


def get_gesture(cap):
    ret, frame = cap.read()
    if not ret:
        return None, None
    RGB_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    x, y = detect_hand_gesture(RGB_frame)
    if x is not None and y is not None:
        if y < int(0.45 * frame.shape[0]):
            return 'up'
    return None


def show_game_over_screen():
    button_color = (200, 200, 200)
    button_hover_color = (150, 150, 150)
    button_text_color = (0, 0, 0)
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 25, 200, 50)
    font = pygame.font.Font(None, 48)

    while True:
        screen.fill(WHITE)
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed()

        if button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, button_hover_color, button_rect)
            if mouse_click[0]:
                return True
        else:
            pygame.draw.rect(screen, button_color, button_rect)

        button_text = font.render("Try Again", True, button_text_color)
        screen.blit(button_text, (button_rect.centerx - button_text.get_width() // 2,
                                 button_rect.centery - button_text.get_height() // 2))

        game_over_text = font.render("Game Over", True, BLACK)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        clock.tick(FPS)


def main():
    def reset_game():
        nonlocal dino, obstacles, clouds, points, game_speed, obstacle_timer, cloud_timer, last_obstacle_type
        dino = Dino()
        obstacles = []
        clouds = []
        points = 0
        game_speed = 10
        obstacle_timer = 0
        cloud_timer = 0
        last_obstacle_type = None
        pygame.mixer.music.play(-1)

    # Initialize Webcam
    cap = cv2.VideoCapture(0)

    # Object
    dino = Dino()
    ground = Ground()
    obstacles = []
    clouds = []

    # Game variable
    game_speed = 10
    points = 0
    previous_gesture = None
    obstacle_timer = 0
    cloud_timer = 0
    last_obstacle_type = None

    cactus_imgs = [
        pygame.transform.scale(pygame.image.load("assets/cactus.png"), (34, 70))
        for i in range(1, 4)
    ]
    bird_imgs = [
        pygame.transform.scale(pygame.image.load("assets/bird.jpeg"), (46, 40)),
        pygame.transform.scale(pygame.image.load("assets/bird.jpeg"), (46, 40))
    ]

    def generate_obstacle():
        nonlocal last_obstacle_type

        bird_probability = min(0.2 + (game_speed - 10) * 0.02, 0.4)

        if last_obstacle_type == "bird":
            bird_probability *= 0.5
        elif last_obstacle_type == "cactus":
            bird_probability *= 1.5

        if random.random() < bird_probability:
            obstacle = Obstacle(bird_imgs[0], "bird")
            last_obstacle_type = "bird"
            height_choice = random.choice(['high', 'medium', 'low'])
            if height_choice == 'high':
                obstacle.rect.y = GROUND_Y - 90
            elif height_choice == 'medium':
                obstacle.rect.y = GROUND_Y - 60
            else:
                obstacle.rect.y = GROUND_Y - 30
        else:
            num_cacti = random.choices([1, 2, 3], weights=[50, 30, 20])[0]
            last_obstacle_type = "cactus"

            if num_cacti == 1:
                obstacle = Obstacle(random.choice(cactus_imgs), "cactus")
            else:
                base_cactus = random.choice(cactus_imgs)
                obstacle = Obstacle(base_cactus, "cactus")
                for i in range(num_cacti - 1):
                    extra_cactus = Obstacle(random.choice(cactus_imgs), "cactus")
                    extra_cactus.rect.x = obstacle.rect.x + (i + 1) * 20
                    obstacles.append(extra_cactus)

        return obstacle

    # Play music
    pygame.mixer.music.play(-1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                cap.release()
                cv2.destroyAllWindows()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    dino.jump()
                if event.key == pygame.K_DOWN:
                    dino.duck()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    dino.stop_duck()

        # Hand Gesture
        gesture = get_gesture(cap)
        if gesture == 'up' and previous_gesture != 'up':
            dino.jump()
        previous_gesture = gesture

        # Update Speed & Score
        game_speed = min(10 + (points // 100), 25)
        points += 1

        # Check for score milestones (50, 100, 150, etc.)
        if points > 0 and points % 500 == 0:  # Multiply by 10 since points increment by 1
            try:
                SCORE_SOUND.play()
            except:
                pass

        min_distance = 500 - (game_speed * 10)
        max_distance = 800 - (game_speed * 5)

        if len(obstacles) == 0 or \
                (obstacle_timer <= 0 and obstacles[-1].rect.x < SCREEN_WIDTH - random.randint(500, 800)):
            obstacles.append(generate_obstacle())
            obstacle_timer = random.randint(40, 80)
        obstacle_timer -= 1

        if cloud_timer <= 0:
            clouds.append(Cloud())
            cloud_timer = random.randint(150, 300)
        cloud_timer -= 1

        # Update Object
        dino.update()
        ground.update(game_speed)

        # Update new obstacle and delete remove old obstacle
        for obstacle in obstacles[:]:
            obstacle.update(game_speed)
            if obstacle.rect.x < -obstacle.rect.width:
                obstacles.remove(obstacle)
            # collision detect
            if dino.rect.colliderect(obstacle.rect):
                try:
                    pygame.mixer.music.stop()
                    DEATH_SOUND.play()
                except:
                    pass
                # Show game over screen and handle restart
                if show_game_over_screen():
                    reset_game()
                    break
                else:
                    running = False
                    break

        for cloud in clouds[:]:
            cloud.update()
            if cloud.x < -cloud.image.get_width():
                clouds.remove(cloud)

        screen.fill(WHITE)
        for cloud in clouds:
            cloud.draw()
        ground.draw()
        for obstacle in obstacles:
            obstacle.draw()
        dino.draw()

        # Display Score
        font = pygame.font.Font(None, 30)
        score_text = font.render(f"Score: {points // 10}", True, BLACK)
        screen.blit(score_text, (SCREEN_WIDTH - 120, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
