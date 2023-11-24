import pygame, random

SCREEN_WIDTH = 626
SCREEN_HEIGHT = 417
WHITE = (255,255,255)
BLACK = (0,0,0)
cord_x = 10
cord_y = 10
x_speed = 0
y_speed = 0


class Meteor(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("meteor.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.x += -1

		if self.rect.x < 0:
			self.rect.x = SCREEN_WIDTH
			self.rect.y = random.randrange(SCREEN_HEIGHT)
          

class Player (pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("player.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()

	def update(self):
		self.rect.x = cord_x
		self.rect.y = cord_y
          
class Laser(pygame.sprite.Sprite):
	def __init__(self):
		super().__init__()
		self.image = pygame.image.load("laser.png").convert()
		self.image.set_colorkey(BLACK)
		self.rect = self.image.get_rect()
	def update(self):
		self.rect.x += 5
		
class Game(object):
	def __init__(self):
		self.start = True
		self.game_over = False
		self.score = 0
		self.lives = 3
		self.meteor_list = pygame.sprite.Group()
		self.all_sprite_list = pygame.sprite.Group()
		self.laser_list = pygame.sprite.Group()
		self.sound = pygame.mixer.Sound("laser5.ogg")
		for i in range(50):
			meteor = Meteor()
			meteor.rect.x = random.randrange(SCREEN_WIDTH) + 400
			meteor.rect.y = random.randrange(SCREEN_HEIGHT)
			self.meteor_list.add(meteor)
			self.all_sprite_list.add(meteor)
		self.player = Player()
		self.all_sprite_list.add(self.player)
	def process_events(self):
		global x_speed,y_speed
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				return True
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT:
					x_speed = -3
				if event.key == pygame.K_RIGHT:
					x_speed = 3
				if event.key == pygame.K_DOWN:
					y_speed = 3
				if event.key == pygame.K_UP:
					y_speed = -3
				if event.key == pygame.K_SPACE:
					laser = Laser()
					laser.rect.x = self.player.rect.x + 45
					laser.rect.y = self.player.rect.y + 45
					self.laser_list.add(laser)
					self.all_sprite_list.add(laser)
					self.sound.play()
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT:
					x_speed = 0
				if event.key == pygame.K_RIGHT:
					x_speed = 0
				if event.key == pygame.K_DOWN:
					y_speed = 0
				if event.key == pygame.K_UP:
					y_speed = 0
			if event.type == pygame.MOUSEBUTTONDOWN:
				if self.game_over:
					self.__init__()
		return False
	def run_logic(self):
		global cord_x,cord_y,x_speed,y_speed
		if not self.game_over:
			for self.laser in self.laser_list:
				meteor_hit_list = pygame.sprite.spritecollide(self.laser, self.meteor_list, True)
				for meteor in meteor_hit_list:
					self.all_sprite_list.remove(self.laser)
					self.laser_list.remove(self.laser)
					self.score += 1
					print(self.score)
				if self.laser.rect.x > SCREEN_WIDTH + 10:
					self.all_sprite_list.remove(self.laser)
					self.laser_list.remove(self.laser)
			if (cord_x > SCREEN_WIDTH or cord_x < -90):
				x_speed *= -1
			if (cord_y > SCREEN_HEIGHT or cord_y < -90):
				y_speed *= -1
			cord_x += x_speed
			cord_y += y_speed
			self.all_sprite_list.update()
			meteor_hit_list = pygame.sprite.spritecollide(self.player, self.meteor_list, True)
			for meteor in meteor_hit_list:
				self.lives -= 1
			if len(self.meteor_list) == 0 or self.lives <= 0:
				self.game_over = True
	def display_frame(self, screen):
		map = pygame.image.load("mapa.jpg").convert()
		begin =pygame.image.load("inicio.png").convert()
		board = (46,204,113)
		red = (255,0,0)
		blue = (46, 134, 193)
		font = pygame.font.SysFont("comicsansms",28)
		font_start = pygame.font.SysFont("comicsansms",50)
		text = font.render("Score: " + str(self.score), True, BLACK)
		text_lives = font.render("Lives: " + str(self.lives), True, WHITE)
		gameover = pygame.image.load("game_over.jpg").convert()
		
		if self.start:
			screen.blit(begin,[0,0])
			start_button = pygame.draw.rect(screen, blue, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT //2, 200, 100), 0)
			text_start = font_start.render("START ", True, WHITE)
			screen.blit(text_start, [SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT //2 + 10] )
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					if start_button.collidepoint(pygame.mouse.get_pos()):
						pygame.draw.rect(screen, (93, 173, 226), start_button,0)
						screen.blit(text_start, [SCREEN_WIDTH // 2 - 90, SCREEN_HEIGHT //2 + 10] )
						self.start = False
		if not self.start:
			screen.blit(map, [0,0])
			if self.game_over:
				screen.blit(gameover,[0,0])
			if not self.game_over:
				self.all_sprite_list.draw(screen)
				pygame.draw.rect(screen,board,(480,10,140,40))
				pygame.draw.rect(screen,red,(10,10,120,40))
				screen.blit(text, [480,10])
				screen.blit(text_lives, [10,10])
		pygame.display.flip()

def main():
	pygame.init()
	screen = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
	done = False
	clock = pygame.time.Clock()
	game = Game()
	while not done:
		done = game.process_events()
		game.run_logic()
		game.display_frame(screen)
		clock.tick(60)
	pygame.quit()

if __name__ == "__main__":
	main()