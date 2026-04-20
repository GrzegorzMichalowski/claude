# Credits:
#
#  Space ship art:
#   Stephen Challener (Redshrike), hosted by OpenGameArt.org
#    CC-BY 3.0
#
#  Asteroid art:
#   Cmdr G
#    CC-BY 3.0
#

import pygame
import random

PLAYER_SPEED = 500  # px / s
ASTEROID_COUNT = 200
ASTEROID_SPEED_X = -200, 200
ASTEROID_SPEED_Y = 50, 300
LASER_SPEED = -400
LASER_COOLDOWN = 0.2
BOOM_FPS = 30
DEBUG = False

class Player:
  def __init__(self, state, x, y):
    self.x = x
    self.y = y
    self.w = 59
    self.h = 42
    self.art = state.assets["ship"]
    self.rect = pygame.Rect(
      x, y, 59, 42
    )

  def logic(self):
    self.rect.x = int(self.x)
    self.rect.y = int(self.y)

  def draw(self, screen):
    screen.blit(
      self.art, (self.x, self.y)
    )

    if DEBUG:
      pygame.draw.rect(screen, (0,255,0), self.rect, width=1)


class Boom:
  def __init__(self, state, x, y, vx, vy):
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
    self.spriteset = state.assets["boom"]
    self.frame = 0
    self.w = 64
    self.h = 64

  def logic(self, dt):
    self.x += self.vx * dt
    self.y += self.vy * dt

    self.frame += BOOM_FPS * dt

    if int(self.frame) >= 16:
      return False

    return True

  def draw(self, screen):
    frame = int(self.frame)

    sx = (frame % 4) * 64
    sy = (frame // 4) * 64

    screen.blit(
      self.spriteset,
      (self.x, self.y),
      area=(sx, sy, 64, 64)
    )

class Laser:
  def __init__(self, state, x, y):
    self.x = x
    self.y = y
    self.asset = state.assets["laser"]
    self.w = self.asset.get_width()
    self.h = self.asset.get_height()
    self.rect = pygame.Rect(
      self.x, self.y, self.w, self.h
    )

  def logic(self, dt):
    self.y += LASER_SPEED * dt

    if self.y < 0 - self.h:
      return False

    self.rect.y = int(self.y)

    return True

  def draw(self, screen):
    screen.blit(self.asset, (self.x, self.y))

    if DEBUG:
      pygame.draw.rect(screen, (255,0,0), self.rect, width=1)

class Asteroid:
  def __init__(self, state, x, y, vx, vy):
    self.x = x
    self.y = y
    self.vx = vx
    self.vy = vy
    self.frames = state.assets["asteroid"]
    self.w = self.frames[0].get_width()
    self.h = self.frames[0].get_height()
    self.rect = pygame.Rect(
      self.x + 16, self.y + 16, self.w - 32, self.h - 32
    )

  def logic(self, dt):
    self.x += self.vx * dt
    self.y += self.vy * dt

    if self.x < 0 - self.w or self.y >= state.h or self.x >= state.w:
      return False

    self.rect.x = int(self.x + 16)
    self.rect.y = int(self.y + 16)

    return True

  def draw(self, screen):
    screen.blit(self.frames[0], (self.x, self.y))

    if DEBUG:
      pygame.draw.rect(screen, (255,255,0), self.rect, width=1)


# Wzor na centrowanie czegos:
# (szer_wiekszego - szer_mniejszego) / 2
# (1280 - 59) // 2

class GameState:
  def __init__(self, screen, assets):
    self.screen = screen
    self.w = screen.get_width()
    self.h = screen.get_height()
    self.ship_w = assets["ship"].get_width()
    self.ship_h = assets["ship"].get_height()
    self.assets = assets
    self.player = Player(
      self,
      (self.w - self.ship_w) // 2,
      self.h - self.ship_h - 40
    )
    self.laser_cooldown = 0

    self.asteroids = []
    self.booms = []
    self.bullets = []

  def logic(self, dt):
    for event in pygame.event.get():
      #print(event)
      if event.type == pygame.QUIT:
        return False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
      return False

    #print(keys[pygame.K_a], dt)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
      self.player.x -= PLAYER_SPEED * dt
      if self.player.x < 0:
        self.player.x = 0

    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
      self.player.x += PLAYER_SPEED * dt
      if self.player.x >= self.w - self.ship_w:
        self.player.x = self.w - self.ship_w

    self.laser_cooldown -= dt
    if keys[pygame.K_SPACE]:
      if self.laser_cooldown <= 0:
        self.laser_cooldown = LASER_COOLDOWN
        bullet = Laser(self,
          self.player.x + (self.player.w - 3) // 2,
          self.player.y + 10
        )
        self.bullets.append(bullet)


    self.player.logic()

    if len(self.asteroids) < ASTEROID_COUNT:
      if random.randint(0, 4) == 0:
        # print(1,2,3)
        # === TO SAMO ↑↓ ===
        # x = 1,2,3
        # print(*x)
        asteroid = Asteroid(
          self,
          random.randint(100, self.w - 164),
          -64,
          random.randint(*ASTEROID_SPEED_X),
          random.randint(*ASTEROID_SPEED_Y)
        )
        self.asteroids.append(asteroid)


    # next_asteroids = []
    # for asteroid in asteroids:
    #   if asteroid.logic():
    #     next_asteroids.append(asteroid)
    # self.asteroids = next_asteroids
    self.asteroids = [
      asteroid for asteroid in self.asteroids if asteroid.logic(dt)
    ]
    # self.asteroids = list(filter(
    #   lambad asteroid: asteroid.logic(dt),
    #   self.asteroids
    # ))

    asteroids_hit = self.player.rect.collidelistall(self.asteroids)
    if asteroids_hit:
      asteroids_hit.sort(reverse=True)
      for idx in asteroids_hit:
        asteroid = self.asteroids.pop(idx)
        boom = Boom(
          self, asteroid.x, asteroid.y,
          asteroid.vx, asteroid.vy
        )
        self.booms.append(boom)

    self.booms = [
      boom for boom in self.booms if boom.logic(dt)
    ]

    self.bullets = [
      bullet for bullet in self.bullets if bullet.logic(dt)
    ]

    for bullet in self.bullets:
      asteroids_hit = bullet.rect.collidelistall(self.asteroids)
      if asteroids_hit:
        asteroids_hit.sort(reverse=True)
        for idx in asteroids_hit:
          asteroid = self.asteroids.pop(idx)
          boom = Boom(
            self, asteroid.x, asteroid.y,
            asteroid.vx, asteroid.vy
          )
          self.booms.append(boom)

          boom = Boom(
            self, bullet.x, bullet.y,
            0, LASER_SPEED
          )
          self.booms.append(boom)

    return True

  def draw(self):
    #screen.fill((0, 255, 0))
    self.screen.blit(self.assets["bg"], (0, 0))

    for bullet in self.bullets:
      bullet.draw(screen)

    self.player.draw(screen)

    for asteroid in self.asteroids:
      asteroid.draw(self.screen)

    for boom in self.booms:
      boom.draw(self.screen)


def init(screen):
  print("Loading...")

  asteroid_anim = []
  for i in range(60):
    fname = f"Asteroid-A-10-{i:02}.png"
    asteroid_anim.append(pygame.image.load(fname))

  assets = {
    "bg": pygame.image.load("bg5.png"),
    "boom": pygame.image.load("exp2_0.png"),
    "asteroid": asteroid_anim,
    "ship": pygame.image.load("shipsheetparts.png"),
    "laser": pygame.image.load("laser.png"),
  }

  state = GameState(screen, assets)

  return state

pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((1280, 720))
state = init(screen)
dt = 0  # delta t

while True:
  if not state.logic(dt):
    break
  state.draw()
  pygame.display.flip()
  dt = clock.tick(60) / 1000

pygame.quit()
