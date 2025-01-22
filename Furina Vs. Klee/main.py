import pygame
import os

pygame.font.init()
pygame.mixer.init()

# Game window dimensions
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chibi Battle")

# Define colors using RGB values
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Create a vertical border/wall in the middle of the screen
BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

# Load sound effects for bullet hits and firing
BULLET_HIT_SOUND = pygame.mixer.Sound(r'Assets\Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound(r'Assets\Gun+Silencer.mp3')

# Set up fonts for health display and winner announcement
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

# Game constants
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 50

# Custom events for hit detection
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

# Load and transform Furina spaceship image
FURINA_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'furina_idle.png'))
FURINA_SPACESHIP = pygame.transform.scale(FURINA_SPACESHIP_IMAGE, (SPACESHIP_WIDTH * 2, SPACESHIP_HEIGHT * 2))

# Load and transform Klee spaceship image
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'klee_idle.png'))
RED_SPACESHIP = pygame.transform.flip(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH * 3, SPACESHIP_HEIGHT * 3)), True, False)

# Load background image
SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

# Load in-game music
GAME_MUSIC = pygame.mixer.Sound(r'Assets\game_music.mp3')


def draw_window(klee, furina, klee_bullets, furina_bullets, klee_health, furina_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    klee_health_text = HEALTH_FONT.render(f"Health: {klee_health}", 1, WHITE)
    furina_health_text = HEALTH_FONT.render(f"Health: {furina_health}", 1, WHITE)
    WIN.blit(klee_health_text, (WIDTH - klee_health_text.get_width() - 10, 10))
    WIN.blit(furina_health_text, (10, 10))

    WIN.blit(FURINA_SPACESHIP, (furina.x, furina.y))
    WIN.blit(RED_SPACESHIP, (klee.x, klee.y))

    for bullet in klee_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in furina_bullets:
        pygame.draw.rect(WIN, BLUE, bullet)

    pygame.display.update()


def furina_handle_movement(keys_pressed, furina):
    if keys_pressed[pygame.K_a] and furina.x - VEL > 0:  # LEFT
        furina.x -= VEL
    if keys_pressed[pygame.K_d] and furina.x + VEL + furina.width < BORDER.x - 80:  # RIGHT (adjusted boundary)
        furina.x += VEL  # Prevent crossing the border
    if keys_pressed[pygame.K_w] and furina.y - VEL > 0:  # UP
        furina.y -= VEL
    if keys_pressed[pygame.K_s] and furina.y + VEL + furina.height < HEIGHT:  # DOWN
        furina.y += VEL


def klee_handle_movement(keys_pressed, klee):
    if keys_pressed[pygame.K_LEFT] and klee.x - VEL > BORDER.x + BORDER.width -20   :  # LEFT
        klee.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and klee.x + VEL + klee.width < WIDTH - 80:  # RIGHT (adjusted boundary)
        klee.x += VEL  # Allowing to go on the border
    if keys_pressed[pygame.K_UP] and klee.y - VEL > 0:  # UP
        klee.y -= VEL
    if keys_pressed[pygame.K_DOWN] and klee.y + VEL + klee.height < HEIGHT:  # DOWN
        klee.y += VEL


def handle_bullets(furina_bullets, klee_bullets, furina, klee):
    for bullet in furina_bullets:
        bullet.x += BULLET_VEL
        if klee.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            furina_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            furina_bullets.remove(bullet)

    for bullet in klee_bullets:
        bullet.x -= BULLET_VEL
        if furina.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            klee_bullets.remove(bullet)
        elif bullet.x < 0:
            klee_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():
    # Initialize the game window
    WIDTH, HEIGHT = 900, 500  # Example dimensions
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Chibi Battle")

    # Create a vertical border/wall in the middle of the screen
    BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

    # Initialize Klee's and Furina's positions
    furina_char = pygame.Rect(50, HEIGHT // 2 - SPACESHIP_HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Left side
    klee_char = pygame.Rect(WIDTH - 150, HEIGHT // 2 - SPACESHIP_HEIGHT // 2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # Right side

    # Initialize other game variables
    klee_bullets = []
    furina_bullets = []
    klee_health = 20
    furina_health = 20

    clock = pygame.time.Clock()
    run = True

    if not pygame.mixer.get_busy():
        GAME_MUSIC.play(-1)

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(furina_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(furina_char.x + furina_char.width, furina_char.y + furina_char.height // 2 - 2, 10, 5)
                    furina_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RCTRL and len(klee_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(klee_char.x, klee_char.y + klee_char.height // 2 - 2, 10, 5)
                    klee_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                klee_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:
                furina_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if klee_health <= 0:
            winner_text = "Furina Wins!"
        if furina_health <= 0:
            winner_text = "Klee Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            GAME_MUSIC.stop()
            return

        keys_pressed = pygame.key.get_pressed()
        furina_handle_movement(keys_pressed, furina_char)
        klee_handle_movement(keys_pressed, klee_char)

        handle_bullets(furina_bullets, klee_bullets, furina_char, klee_char)

        draw_window(klee_char, furina_char, klee_bullets, furina_bullets, klee_health, furina_health)

    GAME_MUSIC.stop()


if __name__ == "__main__":
    main()
    pygame.quit()
