import random
import pygame
import os

class Player(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.startX = x
		self.startY = y
		self.x = x
		self.y = y		
		self.screen_ratio = pygame.display.Info().current_w / pygame.display.Info().current_h
		if self.screen_ratio > 1:
			self.width = int(pygame.display.Info().current_w / 10)
			self.height = self.width
		else: 
			self.width = int(pygame.display.Info().current_h / 10)
			self.height = self.width			
		self.color = '#FFC457'
		self.image = pygame.Surface((int(self.width), int(self.height)))	
		self.image.fill(self.color)
		self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
		self.score = 0
		self.speedX = 0
		self.speedY = 0
		self.damage = 20
		self.direction = 'left'
		self.firewood = 0 
		
	def update(self, blocks):
		self.speedX = 0
		self.speedY = 0
		key = pygame.key.get_pressed()
		if key[pygame.K_LEFT]:
			self.speedX = -5
			self.direction = 'left'
		if key[pygame.K_RIGHT]:
			self.speedX = 5
			self.direction = 'right'
		if key[pygame.K_UP]:
			self.speedY = -5
			self.direction = 'up'
		if key[pygame.K_DOWN]:
			self.speedY = 5
			self.direction = 'down'
		if key[pygame.K_SPACE]:
			self.shoot()
		self.rect.x += self.speedX
		self.collide(self.speedX, 0, blocks)
		self.rect.y += self.speedY
		self.collide(0, self.speedY, blocks)			
		
	def collide(self, speedX, speedY, blocks):
		for block in blocks:
			if pygame.sprite.collide_rect(self, block):
				if speedX > 0:
					self.rect.right = block.rect.left
				if speedX < 0:
					self.rect.left = block.rect.right
				if speedY > 0:
					self.rect.bottom = block.rect.top
				if speedY < 0:
					self.rect.top = block.rect.bottom
				if isinstance(block, Bear):
					self.die()	
					fire.HP = 0				
	
	def shoot(self):
		bullet = Bullet(self.rect.centerx, self.rect.centery, self.direction)
		entities.add(bullet)
		bullets.add(bullet)
	
	def die(self):
		main_menu_bool = True
		self.teleport(self.startX, self.startY)
		fire.HP = 0
		self.score = 0	
				
	def teleport(self, goX, goY):
		self.rect.x = goX
		self.rect.y = goY
	
class Bullet(pygame.sprite.Sprite):
	def __init__(self, x, y, direction):
		self.screen_ratio = pygame.display.Info().current_w / pygame.display.Info().current_h
		if self.screen_ratio > 1:
			self.width = int(pygame.display.Info().current_w / 10)
			self.height = self.width
		else: 
			self.width = int(pygame.display.Info().current_h / 10)
			self.height = self.width
		pygame.sprite.Sprite.__init__(self)	
		self.image = pygame.Surface((self.width - 25, self.height - 25))
		self.image.fill('#FF0000')
		self.startX = x
		self.startY = y
		self.direction = direction
		self.rect = self.image.get_rect(center = (x, y))
		self.speedX = 0
		self.speedY = 0
		self.time = 0
		
	def update(self):
		if self.direction == 'left':
			self.speedX = -100
			if self.rect.x < (self.startX - 100):
				self.kill()
		if self.direction == 'right':
			self.speedX = 10
			if self.rect.x > (self.startX + 50):
				self.kill()
		if self.direction == 'up':
			self.speedY = -10
			if self.rect.y < (self.startY - 100):
				self.kill()
		if self.direction == 'down':
			self.speedY = 10	
			if self.rect.y > (self.startY + 50):
				self.kill()
		self.rect.x += self.speedX
		self.rect.y += self.speedY

class Mountain(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.screen_ratio = pygame.display.Info().current_w / pygame.display.Info().current_h
		if self.screen_ratio > 1:
			self.PLATFORM_width = int(pygame.display.Info().current_w / 10)
			self.PLATFORM_height = self.PLATFORM_width
		else: 
			self.PLATFORM_width = int(pygame.display.Info().current_h / 10)
			self.PLATFORM_height = self.PLATFORM_width		
		self.image = pygame.Surface((int(self.PLATFORM_width), int(self.PLATFORM_height)))	
		self.image.fill('#878787')
		self.rect = self.image.get_rect(x = x, y = y )

class Snow(Mountain):
	def __init__(self, x, y):
		Mountain.__init__(self, x, y)
		self.image = pygame.Surface((int(self.PLATFORM_width), int(self.PLATFORM_height)))	
		self.image.fill('#BAC9FF')
		self.rect = self.image.get_rect(x = x, y = y )

class Pine(Mountain):
	def __init__(self, x, y):
		Mountain.__init__(self, x, y)
		self.x = x
		self.y = y
		#self.Pine_IMG = pygame.image.load('pine1.bmp')
		self.image = pygame.image.load('pine1.gif')#pygame.Surface((int(self.PLATFORM_width), int(self.PLATFORM_height)))	
		self.image.set_colorkey((255,255,255))
		self.image = pygame.transform.scale(self.image, (int(self.PLATFORM_width), int(self.PLATFORM_height)))	
		#self.image.set_colorkey(255,255,255)
		#self.image.fill('#00A00B')
		self.rect = self.image.get_rect(x = self.x, y = self.y)
		self.HP = 100
		
				
class Fire(Mountain):
	def __init__(self, x, y):
		Mountain.__init__(self, x, y)
		self.image = pygame.Surface((int(self.PLATFORM_width), int(self.PLATFORM_height)))	
		self.image.fill('#FFA500')
		self.rect = self.image.get_rect(x = x, y = y )
		self.HP = 100
		self.HP_MAX = 100
		self.prew_state = 0
		self.state = 1	
		self.damage = 1
		self.last_update = pygame.time.get_ticks()
		self.last_update_damage = pygame.time.get_ticks()
		self.minute = 0
		self.sec = 0
	
	def update(self):	
		now = pygame.time.get_ticks()
		if now - self.last_update > 30000:
			self.last_update = now
			prew_damage = self.prew_state
			self.prew_state = self.state
			self.state = self.state + prew_damage
		now_damage = pygame.time.get_ticks()
		if now_damage - self.last_update_damage > 1000:
			self.last_update_damage = now_damage
			self.sec += 1
			self.HP -= (self.state / 4)
			if (self.sec % 60) == 0:
				self.minute += 1	
				self.sec = 0		
	
	def die(self):
		self.HP = 100
		self.HP_MAX = 100
		self.prew_state = 0
		self.state = 1	
		self.minute = 0
		self.sec = 0

class Bear(Mountain):
	def __init__(self, x, y):
		Mountain.__init__(self, x, y)
		self.image = pygame.Surface((int(self.PLATFORM_width), int(self.PLATFORM_height)))	
		self.image.fill('#800000')
		self.rect = self.image.get_rect(x = x, y = y )

class Camera(object):
	def __init__(self, camera_func, width, height):
		self.camera_func = camera_func
		self.state = pygame.Rect(0, 0, width, height)
	
	def apply(self, target):
		return target.rect.move(self.state.topleft)
		
	def update(self, target):
		self.state = self.camera_func(self.state, target.rect)

font_name = pygame.font.match_font('arial')

def draw_text(surf, font_name, text, size, x, y):
	font = pygame.font.Font(font_name, size)
	text_surface = font.render(text, True, '#B70070')
	text_rect = text_surface.get_rect(midtop = (x, y))
	surf.blit(text_surface, text_rect)

def draw_HP_bar(surf, x, y, hp):
	
	BAR_LENGTH = int(width / 4)
	BAR_HEIGHT = int(height / 30)
	fill = (hp / fire.HP_MAX) * BAR_LENGTH
	outline_rect = pygame.Rect(x - (BAR_LENGTH / 2), y, BAR_LENGTH, BAR_HEIGHT)
	fill_rect = pygame.Rect(x - (BAR_LENGTH / 2), y, fill, BAR_HEIGHT)
	if (hp / fire.HP_MAX) < .2:
		pygame.draw.rect(surf, '#FF0007', fill_rect)
		pygame.draw.rect(surf, '#000000', outline_rect, 2)		
	else:
		pygame.draw.rect(surf, '#00FF05', fill_rect)
		pygame.draw.rect(surf, '#000000', outline_rect, 2)

def camera_config(camera, target_rect):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	# for event in pygame.event.get():
		# if event.type == pygame.VIDEORESIZE:
			# width_w, height_w = event.size
	l, t = -l + width / 2, -t + height / 2
	l = min(0, l)
	l = max(-(camera.width - width), l)
	t = min(0, t)
	t = max(-(camera.height - height), t)
	return pygame.Rect(l, t, w, h)


# import sys
W_WIDTH = 800
W_HEIGHT = 480
DIS = (W_WIDTH,W_HEIGHT)
#dis = (width, height)
FPS = 60
pygame.init()
pygame.mixer.init()

width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
#DIS = (width, height)

window = pygame.display.set_mode(DIS, pygame.RESIZABLE)
width, height = window.get_size()
title = "Cheerful Lumberjack"#"GAME size x=%s y=%s"%(width, height)
pygame.display.set_caption(title)
fps = pygame.time.Clock()
#import player
#import blocks
running = True

width = pygame.display.Info().current_w
height = pygame.display.Info().current_h
#DIS = (width, height)
background = '#BAC9FF'
entities = pygame.sprite.Group()
mountains = pygame.sprite.Group()
pines = pygame.sprite.Group()
_fire = pygame.sprite.Group()
bullets = pygame.sprite.Group()	
bears = pygame.sprite.Group()	

# any extra code herre

pygame.display.flip()
pygame.display.update()
new_pine_update = pygame.time.get_ticks()

new_game_run = False
main_menu_bool = True
mouse_pos = 0, 0
score = 0

while running:
	fps.tick(FPS)
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
			raise SystemExit	
	
	while main_menu_bool:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
				raise SystemExit	
			if event.type == pygame.MOUSEBUTTONDOWN:
				mouse_pos = event.pos
				if button.collidepoint(mouse_pos):
					new_game_run = True	
					main_menu_bool = False
		game_canvas = pygame.Surface((width, height))
		bg = pygame.Surface((width, height))
		bg.fill(background)
		game_canvas.blit(bg, (0, 0))	
		window.blit(game_canvas, (0, 0))
		if score > 0:
			draw_text(window, font_name, "YOUR SCORE: " + str(score), int(height / 10), int(width / 2), int(height / 30))
		button = pygame.Rect((width / 2) - (width / 10), (height / 2) - (height / 30), width / 5,  height / 10)
		button_new_game = pygame.draw.rect(window,'#FFFF00', button)	
		draw_text(window, font_name, "NEW GAME", 20, width / 2, height / 2)
		
		pygame.display.flip()
		pygame.display.update()				
	
	if new_game_run:
		new_game_run = False
		score = 0
		damage_modify = 0
		hits1 = None
		hits = None
		all_bloks = []
		level = [
		'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                         H                        M',
		'M                         F                        M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'M                                                  M',
		'MMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMMM']	
		
		game_canvas = pygame.Surface((width, height))
		bg = pygame.Surface((width, height))
		bg.fill(background)
		game_canvas.blit(bg, (0, 0))	
		# screen_ratio = pygame.display.Info().current_w / pygame.display.Info().current_h
		screen_ratio = width / height
		if screen_ratio > 1:
			#PLATFORM_width = int(pygame.display.Info().current_w / 10)
			PLATFORM_width = width / 10
			PLATFORM_height = PLATFORM_width
		else: 
			#PLATFORM_width = int(pygame.display.Info().current_h / 10)
			PLATFORM_width = height / 10
			PLATFORM_height = PLATFORM_width
		# PLATFORM_width = 10
		# PLATFORM_height = PLATFORM_width
		hero = Player(26* PLATFORM_width, 25 * PLATFORM_height)
		x = y = 0
		for row in level:
			for col in row:
				snow = Snow(x, y)
				entities.add(snow)
				if col == "M":
					mountain = Mountain(x, y)
					entities.add(mountain)
					mountains.add(mountain)
					all_bloks.append(mountain)			
				if col == "F":
					fire = Fire(x, y)
					entities.add(fire)
					_fire.add(fire)
					all_bloks.append(fire)	
					fire.HP_MAX = 100
					fire.HP = 100		
				if col == " ":
					rand_mob = random.randrange(0, 101)
					if rand_mob > 99:
						bear = Bear(x, y)
						entities.add(bear)				
						all_bloks.append(bear)	
						bears.add(bear)				
						level[int(y / PLATFORM_width)] = level[int(y / PLATFORM_width)][0 : int(x / PLATFORM_width)] + 'B' + level[int(y / PLATFORM_width)][((int(x / PLATFORM_width)) + 1) : ]
					if rand_mob < 15:
						pine = Pine(x, y)
						entities.add(pine)
						pines.add(pine)
						all_bloks.append(pine)	
						level[int(y / PLATFORM_width)] = level[int(y / PLATFORM_width)][0 : int(x / PLATFORM_width)] + 'P' + level[int(y / PLATFORM_width)][((int(x / PLATFORM_width)) + 1) : ]
						#game_canvas.blit(pine.image, pine)
				x += PLATFORM_width
			y += PLATFORM_height	
			x = 0
		
		entities.add(hero)	
		total_level_width = len(level[0]) * PLATFORM_width
		total_level_height = len(level) * PLATFORM_height
		camera = Camera(camera_config, total_level_width, total_level_height)
		window.blit(game_canvas, (0, 0))		
		
	if (pygame.time.get_ticks() - new_pine_update) > 1000:
		new_pine_update = pygame.time.get_ticks()		
		new_pine_rand = True
		while new_pine_rand:
			y = random.randrange(1, len(level))
			x = random.randrange(1, len(level[0]))
			if level[y][x] == ' ':
				pine = Pine(x * PLATFORM_width, y * PLATFORM_height)
				entities.add(pine)
				pines.add(pine)
				all_bloks.append(pine)	
				level[y] = level[y][ : x] + 'P' + level[y][(x + 1) : ]		
				new_pine_rand = False	
	
	window.blit(game_canvas, (0, 0))			
	hero.update(all_bloks)
	camera.update(hero)
	bullets.update()
	pines.update()	
	_fire.update()	
	
	if fire.HP < 0:
		hero.die()
		fire.die()
		
		main_menu_bool = True
	
	hits1 = pygame.sprite.groupcollide(_fire, bullets, False, True)
	for hit in hits1:
		if hero.firewood > 0:
			hit.HP += hero.firewood
			hero.firewood = 0
			score += 1
			if hit.HP > fire.HP_MAX:
				fire.HP_MAX = hit.HP

	hits = pygame.sprite.groupcollide(pines, bullets, False, True)
	for hit in hits:
		hit.HP = hit.HP - hero.damage - damage_modify
		if 	hit.HP < 0:			
			all_bloks.remove(hit)
			level[int(hit.y / PLATFORM_width)] = level[int(hit.y / PLATFORM_width)][ : int(hit.x / PLATFORM_width)] + ' ' + level[int(hit.y / PLATFORM_width)][((int(hit.x / PLATFORM_width)) + 1) : ]		
			hit.kill()
			hero.firewood = 20
	
	for ent in entities:
		window.blit(ent.image, camera.apply(ent))
	
	draw_text(window, font_name, str(score), int(height / 30), int(width / 4), int(height / 30))
	life_time = str(fire.minute) + ':' + str(fire.sec)
	draw_text(window, font_name, life_time, int(height / 30), int(width * 3 / 4), int(height / 30))
	draw_HP_bar(window, int(width / 2), int(height / 35), fire.HP)
	pygame.display.update()
