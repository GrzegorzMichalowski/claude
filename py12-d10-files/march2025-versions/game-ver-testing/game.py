import pygame
import random
import math

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

img_ship = pygame.image.load("ship.png")
img_bg = pygame.image.load("bg5.jpg").convert()
img_boom = pygame.image.load("exp2_0.png")
img_alamo = pygame.image.load("alamo.png")

img_asteroid = []
for i in range(16):
  img_asteroid.append(pygame.image.load(f"small/a100{i:02}.png"))

font = pygame.font.Font("Quantico-Regular.ttf", 32)

class Missile:
  def __init__(self, x, y, vx, vy):
    self.pos = pygame.Vector2(x, y)
    self.vec = pygame.Vector2(vx, vy)
    self.rect = pygame.Rect(self.pos.x, self.pos.y, 6, 19)

  def blit(self, screen):
    screen.blit(img_alamo, self.pos)
    #pygame.draw.rect(screen, (255,255,0), self.rect, 1)

  def logic(self, dt):
    self.pos += self.vec * dt
    self.rect.x = int(self.pos.x)
    self.rect.y = int(self.pos.y)
    if self.rect.y + 19 < 0:
      return False
    return True


class Boom:
  def __init__(self, x, y, vx, vy):
    self.pos = pygame.Vector2(x, y)
    self.vec = pygame.Vector2(vx, vy)
    self.frame = 0
    self.fps = 16

  def blit(self, screen):
    idx_x = (int(self.frame) % 4) * 64
    idx_y = (int(self.frame) // 4) * 64
    area = pygame.Rect(idx_x, idx_y, 64, 64)
    screen.blit(img_boom, self.pos, area=area)


  def logic(self, dt):
    self.pos += self.vec * dt
    self.frame += dt * self.fps
    if int(self.frame) >= 16:
      return False
    return True


class Asteroid:
  def __str__(self):
    return self.__repr__()

  def __repr__(self):
    return str(self.rect)

  def __init__(self, x, y, vx, vy):
    self.pos = pygame.Vector2(x, y)
    self.vec = pygame.Vector2(vx, vy)
    self.frame_offset = random.randint(0, len(img_asteroid) - 1)
    self.fps = random.randint(5, 30)
    self.inv_fps = 1.0 / self.fps
    self.rect = pygame.Rect(x + 16, y + 16, 32, 32)

  def blit(self, screen, current_time):
    frame = int((self.frame_offset + current_time) * self.fps) % len(img_asteroid)
    img = img_asteroid[frame]
    screen.blit(img, self.pos)
    #pygame.draw.rect(screen, (255,255,0), self.rect, 1)

  def logic(self, dt):
    move = self.vec * dt
    self.pos += move
    self.rect.x = int(self.pos.x + 16)
    self.rect.y = int(self.pos.y + 16)
    if self.pos.y >= screen.get_height():
      return False
    if self.pos.x < -img_asteroid[0].get_width():
      return False
    if self.pos.x > screen.get_width():
      return False
    return True


player_pos = pygame.Vector2(
  (screen.get_width() - img_ship.get_width()) / 2,
  screen.get_height() - img_ship.get_height() - 50
)


SPEED = 3
it = 0

def clamp(a, v, b):
  if v < a:
    return a
  if v > b:
    return b
  return v

current_time = 0
asteroids = []
shots = []
booms = []

ASTEROID_COUNT = 200
COOLDOWN = 0.1

last_score = None
points = 0
shoot_cooldown = 0

while running:
  current_time += dt
  it += 1
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      running = False

  # Logic.
  keys = pygame.key.get_pressed()
  if keys[pygame.K_a]:
    player_pos.x -= 300 * dt
    if player_pos.x < 0:
      player_pos.x = 0

  if keys[pygame.K_d]:
    player_pos.x += 300 * dt
    max_pos_x = screen.get_width() - img_ship.get_width()
    if player_pos.x > max_pos_x:
      player_pos.x = max_pos_x

  if len(asteroids) < ASTEROID_COUNT and random.randint(0, 5) == 0:
    asteroid = Asteroid(
      random.randint(0, screen.get_width() - img_asteroid[0].get_width()),
      random.randint(-100, -50),
      random.randint(-20, 20),
      random.randint(10, 100)
    )
    asteroids.append(asteroid)


  next_asteroids = []
  for asteroid in asteroids:
    if asteroid.logic(dt):
      next_asteroids.append(asteroid)

  asteroids = next_asteroids

  shoot_cooldown -= dt
  if keys[pygame.K_SPACE]:
    if shoot_cooldown <= 0.0:
      shoot_cooldown = COOLDOWN
      shots.append(Missile(player_pos.x, player_pos.y, 0, -180))

  shots = list(filter(lambda shot: shot.logic(dt), shots))

  live_shots = []
  for missile in shots:
    asteroids_hit = missile.rect.collidelistall(asteroids)
    if asteroids_hit:
      asteroids_hit.sort(reverse=True)
      booms.append(Boom(missile.pos.x, missile.pos.y, missile.vec.x, missile.vec.y))
      for idx in asteroids_hit:
        asteroid = asteroids.pop(idx)
        booms.append(Boom(asteroid.pos.x, asteroid.pos.y, asteroid.vec.x, asteroid.vec.y))
        points += 1
    else:
      live_shots.append(missile)

  shots = live_shots




  player_rect = pygame.Rect(player_pos.x, player_pos.y, img_ship.get_width(), img_ship.get_height())

  hit = player_rect.collidelistall(asteroids)

  if hit:
    hit.sort(reverse=True)
    for idx in hit:
      asteroid = asteroids.pop(idx)
      booms.append(Boom(asteroid.pos.x, asteroid.pos.y, asteroid.vec.x, asteroid.vec.y))

  booms = list(filter(lambda boom: boom.logic(dt), booms))


  # Draw.
  source_area = pygame.Rect(
    0, img_bg.get_height() - screen.get_height() - current_time, screen.get_width(), screen.get_height()
  )

  if not hit:
    screen.blit(img_bg, (0, 0), source_area)
  else:
    screen.fill(0xffffff)

  for missile in shots:
    missile.blit(screen)

  #pygame.draw.rect(screen, (255,255,0), player_rect, 1)
  screen.blit(img_ship, player_pos)

  for asteroid in asteroids:
    asteroid.blit(screen, current_time)

  for boom in booms:
    boom.blit(screen)

  text = f"Score: {points}"
  if last_score != text:
    last_score = text
    score = font.render(text, True, (255,255,255))
  screen.blit(score, (10, 10))

  pygame.display.flip()

  dt = clock.tick(60) / 1000

pygame.quit()
