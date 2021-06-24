import pygame as pg
from settings import *
from random import choice, randrange, uniform
from os import path
vec = pg.math.Vector2

img_dir = path.join(path.dirname(__file__), 'img')

class Spritesheet:
    def __init__(self, filename):
        self.spritesheet = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        image = pg. transform.scale(image, (width // 2, height // 2))
        return image

class Spritesheet2:
    def __init__(self, filename):
        self.spritesheet2 = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet2, (0, 0), (x, y, width, height))
        image = pg. transform.scale(image, (width // 2, height // 2))
        return image

class Spritesheet3:
    def __init__(self, filename):
        self.spritesheet3 = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet3, (0, 0), (x, y, width, height))
        image = pg. transform.scale(image, (width // 2, height // 2))
        return image

class Spritesheet4:
    def __init__(self, filename):
        self.spritesheet4 = pg.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        image = pg.Surface((width, height))
        image.blit(self.spritesheet4, (0, 0), (x, y, width, height))
        image = pg. transform.scale(image, (width // 2, height // 2))
        return image

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = PLAYER_LAYER
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.walking = False
        self.jumping = False
        self.health = 100
        self.target_health = 100
        self.max_health = 100
        self.health_bar_length = 100
        self.health_ratio = self.max_health / self.health_bar_length
        self.health_change_speed = 1
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.spawn_timer = 0
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.center = (40, HEIGHT - 100)
        self.pos = vec(40, HEIGHT - 100)
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

    def load_images(self):
        self.standing_frames = [self.game.spritesheet.get_image(40, 29, 83, 154),
                                self.game.spritesheet.get_image(40, 29, 83, 154)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_r = [self.game.spritesheet.get_image(46, 380, 79, 149),
                              self.game.spritesheet.get_image(184, 380, 77, 149),
                              self.game.spritesheet.get_image(320, 380, 78, 149),
                              self.game.spritesheet.get_image(457, 377, 78, 153),
                              self.game.spritesheet.get_image(590, 378, 78, 151),
                              self.game.spritesheet.get_image(729, 381, 78, 149),
                              self.game.spritesheet.get_image(861, 378, 78, 151),
                              self.game.spritesheet.get_image(999, 380, 79, 148)]
        self.walk_frames_l = []
        for frame in self.walk_frames_r:
            frame.set_colorkey(BLACK)
            self.walk_frames_l.append(pg.transform.flip(frame, True, False))
        self.fight_frames_r = [self.game.spritesheet.get_image(1002, 556, 94, 149),
                               self.game.spritesheet.get_image(591, 556, 81, 149),
                               self.game.spritesheet.get_image(726, 556, 107, 148),
                               self.game.spritesheet.get_image(864, 556, 106, 149)]
        self.fight_frames_l = []
        for frame in self.fight_frames_r:
            frame.set_colorkey(BLACK)
            self.fight_frames_l.append(pg.transform.flip(frame, True, False))
        self.jump_frame = self.game.spritesheet.get_image(168, 29, 84, 154)
        self.jump_frame.set_colorkey(BLACK)

    def jump_cut(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

    def jump(self):
        self.rect.x += 2
        hits = pg.sprite.spritecollide(self, self.game.platforms, False)
        hits2 = pg.sprite.spritecollide(self, self.game.spawns, False)
        self.rect.x -= 2
        if hits and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.image = self.jump_frame
            self.vel.y = -PLAYER_JUMP
        if hits2 and not self.jumping:
            self.game.jump_sound.play()
            self.jumping = True
            self.image = self.jump_frame
            self.vel.y = -PLAYER_JUMP

    def update(self):
        now = pg.time.get_ticks()
        self.animate()
        self.acc = vec(0, PLAYER_GRAV)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT]:
            self.acc.x = -PLAYER_ACC
        if keys[pg.K_RIGHT]:
            self.acc.x = PLAYER_ACC

        self.acc += self.vel * PLAYER_FRICTION
        self.vel += self.acc
        if abs(self.vel.x) < 0.1:
            self.vel.x = 0
        self.pos += self.vel +0.5 * self.acc
        if self.pos.x > WIDTH + self.rect.width / 2:
            self.pos.x = 0 - self.rect.width / 2
        if self.pos.x < 0 - self.rect.width / 2:
            self.pos.x = WIDTH + self.rect.width / 2
        self.rect.midbottom = self.pos
  
    def animate(self):
        now = pg.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 180:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom

        if not self.jumping and not self.walking:
            if now - self.last_update > 350:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                bottom = self.rect.bottom
                self.image = self.standing_frames[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
        self.mask = pg.mask.from_surface(self.image)

class Cloud(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = CLOUD_LAYER
        self.groups = game.all_sprites, game.clouds
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = choice(self.game.cloud_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        scale = randrange(50, 101) / 100
        self.image = pg.transform.scale(self.image, (int(self.rect.width * scale),
                                                     int(self.rect.height * scale)))
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-500, -50)

    def update(self):
        if self.rect.top > HEIGHT * 2:
            self.kill()

class Platform(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.platforms
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet2.get_image(0, 288, 380, 94),
                  self.game.spritesheet2.get_image(213, 1662, 201, 100)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        if randrange(100) < POW_SPAWN_PCT:
            Pow(self.game, self)
        if randrange(100) < Goblin_spawn_pct:
            Goblin(self.game, self)
        if randrange(100) < Health_spawn_pct:
            Powhp(self.game, self)

class Spawn(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLATFORM_LAYER
        self.groups = game.all_sprites, game.spawns
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        images = [self.game.spritesheet2.get_image(0, 288, 380, 94),
                  self.game.spritesheet2.get_image(213, 1662, 201, 100)]
        self.image = choice(images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Goblin(pg.sprite.Sprite):
    def __init__(self, game, plat):
        self._layer = MOB_LAYER
        self.groups = game.all_sprites, game.goblins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.walking = False
        self.current_frame = 0
        self.last_update = 0
        self.load_images()
        self.image = self.standing_frames[0]
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top
        self.move = randrange(-1, 1)
        if self.move == 0:
            self.move = 1

    def load_images(self):
        self.standing_frames = [self.game.spritesheet4.get_image(64, 58, 168, 146),
                                self.game.spritesheet4.get_image(55, 580, 169, 149)]
        for frame in self.standing_frames:
            frame.set_colorkey(BLACK)
        self.walk_frames_l = [self.game.spritesheet4.get_image(60, 235, 163, 148),
                              self.game.spritesheet4.get_image(250, 237, 165, 147),
                              self.game.spritesheet4.get_image(447, 239, 162, 147),
                              self.game.spritesheet4.get_image(634, 237, 163, 145),
                              self.game.spritesheet4.get_image(62, 412, 165, 145),
                              self.game.spritesheet4.get_image(251, 404, 165, 146),
                              self.game.spritesheet4.get_image(444, 406, 163, 146),
                              self.game.spritesheet4.get_image(632, 405, 162, 147)]
        self.walk_frames_r = []
        for frame in self.walk_frames_l:
            frame.set_colorkey(BLACK)
            self.walk_frames_r.append(pg.transform.flip(frame, True, False))
        self.fight_frames_l =[self.game.spritesheet4.get_image(64, 58, 168, 146),
                              self.game.spritesheet4.get_image(263, 59, 157, 145),
                              self.game.spritesheet4.get_image(447, 58, 150, 149),
                              self.game.spritesheet4.get_image(629, 62, 166, 147)]
        for frame in self.fight_frames_l:
            frame.set_colorkey(BLACK)

    def update(self):
        self.animate()
        self.rect.x += self.move
        if self.rect.x == self.plat.rect.left - 20:
            self.move = 1
        if self.rect.x >= self.plat.rect.right - 55:
            self.move = -1
        self.rect.bottom = self.plat.rect.top
        if not self.game.platforms.has(self.plat):
            self.kill()

    def animate(self):
        now = pg.time.get_ticks()
        if self.move != 0:
            self.walking = True
        else:
            self.walking = False
        if self.walking:
            if now - self.last_update > 100:
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames_l)

                if self.move > 0:
                    self.image = self.walk_frames_r[self.current_frame]
                else:
                    self.image = self.walk_frames_l[self.current_frame]
        self.mask = pg.mask.from_surface(self.image)
    
class Pow(pg.sprite.Sprite):
    def __init__ (self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['boost'])
        self.image = pg.image.load(path.join(img_dir, 'blue_gem_7.png')).convert()
        self.image = pg.transform.scale(self.image, (53, 53))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx
        self.rect.bottom = self.plat.rect.top 
        

    def update(self):
        self.rect.bottom = self.plat.rect.top
        if not self.game.platforms.has(self.plat):
            self.kill()

class Powhp(pg.sprite.Sprite):
    def __init__ (self, game, plat):
        self._layer = POW_LAYER
        self.groups = game.all_sprites, game.powerhps
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.plat = plat
        self.type = choice(['health'])
        self.image = pg.image.load(path.join(img_dir, 'green_gem_2.png')).convert()
        self.image = pg.transform.scale(self.image, (48, 45))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.plat.rect.centerx -15
        self.rect.bottom = self.plat.rect.top 
        

    def update(self):
        self.rect.bottom = self.plat.rect.top
        if not self.game.platforms.has(self.plat):
            self.kill()
     
class Mob(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups= game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_up = self.game.spritesheet3.get_image(713, 1001, 300, 223)
        self.image_up = pg.transform.scale(self.image_up, (120, 89))
        self.image_up.set_colorkey(BLACK)
        self.image_down = self.game.spritesheet3.get_image(715, 1244, 301, 205)
        self.image_down = pg.transform.scale(self.image_down, (120, 82))
        self.image_down.set_colorkey(BLACK)
        self.image = self.image_up
        self.rect = self.image.get_rect()
        self.rect.centerx = choice([-100, WIDTH + 100])
        self.vx = randrange(1, 4)
        if self.rect.centerx > WIDTH:
            self.vx *= -1
        self.rect.y = randrange(HEIGHT / 2)
        self.vy = 0
        self.dy = 0.5
    def update(self):
        if self.rect.centerx == WIDTH + 100:
            self.image_up = pg.transform.flip(self.image_up, True, False)
            self.image_down = pg.transform.flip(self.image_down, True, False)
        self.rect.x += self.vx
        self.vy += self.dy
        if self.vy > 3 or self.vy < -3:
            self.dy *= -1
        center = self.rect.center
        if self.dy < 0:
            self.image = self.image_up
        else:
            self.image = self.image_down
        self.rect = self.image.get_rect()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.center = center
        self.rect.y += self.vy
        if self.rect.left > WIDTH + 100 or self.rect.right < -100:
            self.kill()

class Rock(pg.sprite.Sprite):
    def __init__(self, game):
        self._layer = MOB_LAYER
        self.groups= game.all_sprites, game.rocks
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image_orig = pg.image.load(path.join(img_dir, 'meteorBig.png'))
        self.image_orig = pg.transform.scale(self.image_orig, (90, 75))
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.rect.x = randrange(WIDTH - self.rect.width)
        self.rect.y = randrange(-100, -40)
        self.speedy = randrange(3, 5)
        self.rot = 0
        self.rot_speed = randrange(-8, 8)
        self.last_update = pg.time.get_ticks()

    def update(self):
        self.rotate()
        self.mask = pg.mask.from_surface(self.image)
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = randrange(WIDTH - self.rect.width)
            self.rect.y = randrange(-100, -40)
            self.speedy = randrange(3, 5)
      
        if self.rect.bottom > HEIGHT + 100:
            self.kill()

    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center