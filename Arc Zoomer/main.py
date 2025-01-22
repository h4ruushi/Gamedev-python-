import random
import pygame

from objects import Player, Balls, Dot, Shadow, Particle, Message, BlinkingText, Button

pygame.init()
SCREEN = WIDTH, HEIGHT = 288, 512
CENTER = WIDTH //2, HEIGHT // 2

info = pygame.display.Info()
width = info.current_w
height = info.current_h

if width >= height:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME)
else:
	win = pygame.display.set_mode(SCREEN, pygame.NOFRAME | pygame.SCALED | pygame.FULLSCREEN)

clock = pygame.time.Clock()
FPS = 90

# SCREENCOLORS **********************************************************************


GREEN = (0,177,64)
BLUE = (30, 144,255)
ORANGE = (252,76,2)
PURPLE = (155,38,182)
AQUA = (0,103,127)
WHITE = (255,255,255)
BLACK = (0,0,0)

color_list = [GREEN, BLUE, ORANGE, PURPLE]
color_index = 0
color = color_list[color_index]

# Define neon colors
NEON_BLUE = (0, 255, 255)  # Cyan color for neon blue
NEON_PINK = (255, 20, 147)  # Deep pink color for neon pink

# FONTS ***********************************************************************

title_font = "Fonts/Aladin-Regular.ttf"
tap_to_play_font = "Fonts/BubblegumSans-Regular.ttf"
score_font = "Fonts/DalelandsUncialBold-82zA.ttf"
game_over_font = "Fonts/ghostclan.ttf"

# MESSAGES ********************************************************************

tap_to_play = BlinkingText(WIDTH//2, HEIGHT-60, 20, "Click Mouse to play", tap_to_play_font, WHITE, win)
game_msg = Message(80, 150, 40, "GAME", game_over_font, NEON_BLUE, win)
over_msg = Message(210, 150, 40, "OVER!", game_over_font, NEON_PINK, win)
score_text = Message(90, 230, 20, "SCORE", None, BLACK, win)
best_text = Message(200, 230, 20, "BEST", None, BLACK, win)

score_msg = Message(WIDTH-60, 50, 50, "0", score_font, WHITE, win)
final_score_msg = Message(90, 280, 40, "0", tap_to_play_font, BLACK, win)
high_score_msg = Message(200, 280, 40, "0", tap_to_play_font, BLACK, win)

# SOUNDS **********************************************************************

score_fx = pygame.mixer.Sound('Sounds/point.mp3')
death_fx = pygame.mixer.Sound('Sounds/dead.mp3')
score_page_fx = pygame.mixer.Sound('Sounds/score_page.mp3')

pygame.mixer.music.load('Sounds/hk.mp3')
pygame.mixer.music.play(loops=-1)
pygame.mixer.music.set_volume(0.5)

# Button images

home_img = pygame.image.load('Assets/homeBtn.png')
replay_img = pygame.image.load('Assets/replay.png')
sound_off_img = pygame.image.load("Assets/soundOffBtn.png")
sound_on_img = pygame.image.load("Assets/soundOnBtn.png")
title_img = pygame.image.load('Assets/title.png')
title_img = pygame.transform.scale(title_img, (400, 300))

# Buttons

home_btn = Button(home_img, (24, 24), WIDTH // 4 - 18, 390)
replay_btn = Button(replay_img, (36,36), WIDTH // 2  - 18, 382)
sound_btn = Button(sound_on_img, (24, 24), WIDTH - WIDTH // 4 - 18, 390)

# GAME VARIABLES **************************************************************

MAX_RAD = 120
rad_delta = 50
additional_balls_active_20 = False
additional_balls_active_50 = False
resetting = False

# OBJECTS *********************************************************************

ball_group = pygame.sprite.Group()
dot_group = pygame.sprite.Group()
shadow_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
p = Player(win)

def create_initial_balls():
	ball_group.empty()
	ball_positions = [(CENTER[0], CENTER[1]-75), (CENTER[0], CENTER[1]+75)]
	for pos in ball_positions:
		ball = Balls(pos, 2, 1, win)
		ball_group.add(ball)

def create_additional_balls():
	additional_positions = [(CENTER[0]-105, CENTER[1]), (CENTER[0]+105, CENTER[1]),
							(CENTER[0]-45, CENTER[1]), (CENTER[0]+45, CENTER[1])]
	for pos in additional_positions:
		ball = Balls(pos, 1, 3, win)
		ball_group.add(ball)

create_initial_balls()

dot_list = [(CENTER[0], CENTER[1]-MAX_RAD+3), (CENTER[0]+MAX_RAD-3, CENTER[1]),
			(CENTER[0], CENTER[1]+MAX_RAD-3), (CENTER[0]-MAX_RAD+3, CENTER[1])]
dot_index = random.choice([1,2,3,4])
dot_pos = dot_list[dot_index-1]
dot = Dot(*dot_pos, win)
dot_group.add(dot)

shadow = Shadow(dot_index, win)
shadow_group.add(shadow)


# VARIABLES *******************************************************************

clicked = False
num_clicks = 0
player_alive = True
sound_on = True

score = 0
highscore = 0

home_page = True
game_page = False
score_page = False

running = True
while running:
	win.fill(BLACK)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE or \
				event.key == pygame.K_q:
				running = False

		if event.type == pygame.MOUSEBUTTONDOWN and home_page:
			home_page = False
			game_page = True
			score_page = False

			rad_delta = 50
			clicked = True
			score = 0
			num_clicks = 0
			player_alive = True
			additional_balls_active_20 = False
			additional_balls_active_50 = False
			create_initial_balls()

		if event.type == pygame.MOUSEBUTTONDOWN and game_page:
			if not clicked:
				clicked = True
				for ball in ball_group:
					if num_clicks % ball.inverter == 0:
						ball.dtheta *= -1

				p.set_move(dot_index)

				num_clicks += 1
				if num_clicks % 5 == 0:
					color_index += 1
					if color_index > len(color_list) - 1:
						color_index = 0

					color = color_list[color_index]

		if event.type == pygame.MOUSEBUTTONDOWN and game_page:
			clicked = False

	if home_page:
		title_x = (WIDTH // 2) - (title_img.get_width() // 2)
		title_y = (HEIGHT // 2) - (title_img.get_height() // 2)
		win.blit(title_img, (title_x, title_y))
		tap_to_play.update()

	if score_page:
		game_msg.update()
		over_msg.update()
		score_text.update(shadow=False)
		best_text.update(shadow=False)

		final_score_msg.update(score, shadow=False)
		high_score_msg.update(highscore, shadow=False)

		if home_btn.draw(win):
			home_page = True
			score_page = False
			game_page = False
			score = 0
			additional_balls_active_20 = False
			additional_balls_active_50 = False
			create_initial_balls()
			score_msg = Message(WIDTH-60, 50, 50, "0", score_font, WHITE, win)

		if replay_btn.draw(win):
			home_page = False
			score_page = False
			game_page = True

			player_alive = True
			score = 0
			additional_balls_active_20 = False
			additional_balls_active_50 = False
			create_initial_balls()
			score_msg = Message(WIDTH-60, 50, 50, "0", score_font, WHITE, win)
			p = Player(win)

		if sound_btn.draw(win):
			sound_on = not sound_on
			
			if sound_on:
				sound_btn.update_image(sound_on_img)
				pygame.mixer.music.play(loops=-1)
			else:
				sound_btn.update_image(sound_off_img)
				pygame.mixer.music.stop()

	if game_page:

		for radius in [30 + rad_delta, 60 + rad_delta, 90 + rad_delta, 120 + rad_delta]:
			if rad_delta > 0:
				radius -= 1
				rad_delta -= 1
			pygame.draw.circle(win, color, CENTER, radius, 5)


		pygame.draw.rect(win, color, [CENTER[0]-10, CENTER[1]-MAX_RAD, 20, MAX_RAD*2])
		pygame.draw.rect(win, color, [CENTER[0]-MAX_RAD, CENTER[1]-10, MAX_RAD*2, 20])

		if rad_delta <= 0:
			p.update(player_alive, color, shadow_group)
			shadow_group.update()
			ball_group.update()
			dot_group.update()
			particle_group.update()
			score_msg.update(score)

			for dot in dot_group:
				if dot.rect.colliderect(p):
					dot.kill()
					score_fx.play()

					score += 1
					if score == 20 and not additional_balls_active_20 and not resetting:
						print("Score reached 20, resetting player and adding additional balls.")
						resetting = True
						p.reset()
						dot_group.empty()
						shadow_group.empty()
						additional_balls_active_20 = True
						create_additional_balls()
						dot_index = random.randint(1,4)
						dot_pos = dot_list[dot_index-1]
						dot = Dot(*dot_pos, win)
						dot_group.add(dot)
						shadow = Shadow(dot_index, win)
						shadow_group.add(shadow)
					if score == 50 and not additional_balls_active_50:
						print("Score reached 50, adding additional balls.")
						p.reset()
						dot_group.empty()
						shadow_group.empty()
						additional_balls_active_50 = True
						create_additional_balls()
						create_additional_balls()
					if highscore <= score:
						highscore = score

			if pygame.sprite.spritecollide(p, ball_group, False) and player_alive:
				death_fx.play()
				x, y = p.rect.center
				for i in range(20):
					particle = Particle(x, y, WHITE, win)
					particle_group.add(particle)
				player_alive = False
				p.reset()

			if p.can_move and len(dot_group) == 0 and player_alive:
				dot_index = random.randint(1,4)
				dot_pos = dot_list[dot_index-1]
				dot = Dot(*dot_pos, win)
				dot_group.add(dot)

				shadow_group.empty()
				shadow = Shadow(dot_index, win)
				shadow_group.add(shadow)

			if not player_alive and len(particle_group) == 0:
				game_page = False
				score_page = True

				dot_group.empty()
				shadow_group.empty()
				for ball in ball_group:
					ball.reset()
				score_page_fx.play()


	pygame.draw.rect(win, WHITE, (0, 0, WIDTH, HEIGHT), 5, border_radius=10)
	clock.tick(FPS)
	pygame.display.update()

pygame.quit()