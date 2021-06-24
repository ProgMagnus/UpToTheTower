import pygame as pg
import random
import sys
from settings import *
from sprites import *
from os import path
import pickle

jump_image = pg.image.load(path.join(img_dir, 'blue_gem_7.png'))
jump_image = pg.transform.scale(jump_image, (39, 39))
jump_image.set_colorkey(BLACK)

class Game:
    def __init__(self):
        pg.init()
        pg.mixer.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        self.running = True
        self.load_data()

    def pause(self):
        self.screen.fill(BLACK)
        self.draw_text( 'PAUSE', 18, WIDTH / 2, HEIGHT / 2)
        self.draw_text2( 'Press any key to continue', 22, WIDTH / 2, 550)
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                if event.type == pg.KEYDOWN:
                    waiting = False
    
    def info(self):
        self.screen.blit(info_screen, info_screen_rect)
        self.draw_text2( 'Fatal damage', 22, WIDTH/2 + 100, 60)
        self.draw_text2( '-25 HP', 22, WIDTH/2 + 100, 155)
        self.draw_text2( '+25 HP', 22, WIDTH/2 + 100, 240)
        self.draw_text2( '+1 Power Jump', 22, WIDTH/2 + 100, 315)

        self.draw_text2( 'Arrows', 22, WIDTH/2 - 150, 390)
        self.draw_text2( 'Space', 22, WIDTH/2 - 150, 430)
        self.draw_text2( 'W', 22, WIDTH/2 - 150, 470)
        self.draw_text2( 'S', 22, WIDTH/2 - 150, 510)
        self.draw_text2( 'I', 22, WIDTH/2 - 150, 550)

        self.draw_text2( 'Move', 22, WIDTH/2 + 100, 390)
        self.draw_text2( 'Jump', 22, WIDTH/2 + 100, 430)
        self.draw_text2( 'Power Jump', 22, WIDTH/2 + 100, 470)
        self.draw_text2( 'Pause', 22, WIDTH/2 + 100, 510)
        self.draw_text2( 'Info', 22, WIDTH/2 + 100, 550)
        pg.display.flip()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    waiting = False

    def advanced_health(self):
        transition_width = 0
        transition_color = RED

        if self.player.health < self.player.target_health:
            self.player.health += self.player.health_change_speed
        if self.player.health > self.player.target_health:
            self.player.health -= self.player.health_change_speed

        health_bar_rect = pg.Rect(465,557, self.player.health/self.player.health_ratio, 25)
        transition_bar_rect = pg.Rect(health_bar_rect.right, 557, transition_width, 25)
        pg.draw.rect(self.screen, GREEN, health_bar_rect)
        pg.draw.rect(self.screen, transition_color, transition_bar_rect)
        pg.draw.rect(self.screen, WHITE,(465,557, self.player.health_bar_length, 25), 4)

    def load_data(self):
        self.dir = path.dirname(__file__)
        img_dir = path.join(self.dir, 'img')
        with open(path.join(self.dir, HS_FILE), 'r') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0
        self.spritesheet = Spritesheet(path.join(img_dir, KNIGHT))
        self.spritesheet2 = Spritesheet2(path.join(img_dir, Ground))
        self.spritesheet3 = Spritesheet3(path.join(img_dir, Mobster))
        self.spritesheet4 = Spritesheet3(path.join(img_dir, Goblins))
        self.cloud_images = []
        for i in range(1, 4):
            self.cloud_images.append(pg.image.load(path.join(img_dir, 'cloud{}.png'.format(i))).convert())
        self.snd_dir = path.join(self.dir, 'snd')
        self.jump_sound = pg.mixer.Sound(path.join(self.snd_dir, 'BounceYoFrankie.wav'))
        self.boost_sound = pg.mixer.Sound(path.join(self.snd_dir, 'Rise01.wav'))
        self.hit_sound = pg.mixer.Sound(path.join(self.snd_dir, 'hit1.wav'))

    def new(self):
        self.score = 0
        self.jump_count = 0
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.platforms = pg.sprite.Group()
        self.spawns = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.powerhps = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.rocks = pg.sprite.Group()
        self.goblins = pg.sprite.Group()
        self.clouds = pg.sprite.Group()
        self.player = Player(self)
        for plat in PLATFORM_LIST:
            Platform(self, *plat)
        for spaw in SPAWN_POINT:
            Spawn(self, *spaw)
        self.mob_timer = 0
        self.rock_timer = 0
        pg.mixer.music.load(path.join(self.snd_dir, 'RPG.ogg'))
        for i in range(8):
            c = Cloud(self)
            c.rect.y += 500
        self.run()

    def run(self):
        pg.mixer.music.play(loops=-1)
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()
        pg.mixer.music.fadeout(500)

    def update(self):
        self.all_sprites.update()

        now = pg.time.get_ticks()
        if now - self.mob_timer > 7000 + random.choice([-1000, -500, 0, 500, 1000]):
            self.mob_timer = now
            Mob(self)

        now = pg.time.get_ticks()
        if now - self.rock_timer > 28000 + random.choice([-100, -75, 0, 75, 100]):
            self.rock_timer = now
            Rock(self)

        goblins_hits = pg.sprite.spritecollide(self.player, self.goblins, False, pg.sprite.collide_mask)
        if goblins_hits:
            self.hit_sound.play()
            if self.player.target_health > 0:
                    self.player.target_health -= 25
            if self.player.target_health <=0:
                    self.player_target_health = 0
                    self.playing = False
 
            if self.player.acc.x !=0:
                if self.player.acc.x > 0 and self.player.vel.x > 0:
                    self.player.vel.x -= 10
                else :
                    self.player.vel.x += 10

            if self.player.vel.y !=0:
                if self.player.vel.y > 0:
                    self.player.vel.y -=30
                else:
                    self.player.vel.y +=30

            elif self.player.acc.x == 0: #stay - work
                self.player.vel.y -=30
            
        rock_hits = pg.sprite.spritecollide(self.player, self.rocks, False, pg.sprite.collide_mask)
        if rock_hits:
            self.hit_sound.play()
            self.playing = False

        mob_hits = pg.sprite.spritecollide(self.player, self.mobs, False, pg.sprite.collide_mask)
        if mob_hits:
            self.hit_sound.play()
            if self.player.target_health > 0:
                    self.player.target_health -= 25
            if self.player.target_health <=0:
                    self.player_target_health = 0
                    self.playing = False
 
            if self.player.acc.x !=0:
                if self.player.acc.x > 0 and self.player.vel.x > 0:
                    self.player.vel.x -= 10
                else :
                    self.player.vel.x += 10

            if self.player.vel.y !=0:
                if self.player.vel.y > 0:
                    self.player.vel.y -=30
                else:
                    self.player.vel.y +=30

            elif self.player.acc.x == 0: #stay - work
                self.player.vel.y -=30

        if self.player.vel.y > 0:
            hits = pg.sprite.spritecollide(self.player, self.platforms, False)
            hits2 = pg.sprite.spritecollide(self.player, self.spawns, False)
            if hits:
                lowest = hits[0]
                for hit in hits:
                    if hit.rect.bottom > lowest.rect.bottom:
                        lowest = hit
                if self.player.pos.x < lowest.rect.right + 10 and \
                   self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False
            if hits2:
                lowest = hits2[0]
                for hit2 in hits2:
                    if hit2.rect.bottom > lowest.rect.bottom:
                        lowest = hit2
                if self.player.pos.x < lowest.rect.right + 10 and \
                   self.player.pos.x > lowest.rect.left - 10:
                    if self.player.pos.y < lowest.rect.centery:
                        self.player.pos.y = lowest.rect.top
                        self.player.vel.y = 0
                        self.player.jumping = False

        if self.player.rect.top <= HEIGHT / 2:
            if random.randrange(100) < 15:
                Cloud(self)
            self.player.pos.y += max(abs(self.player.vel.y), 2)
            for cloud in self.clouds:
                cloud.rect.y += max(abs(self.player.vel.y / 2), 2)
            for mob in self.mobs:
                mob.rect.y += max(abs(self.player.vel.y), 2)
            for rock in self.rocks:
                rock.rect.y += max(abs(self.player.vel.y), 2)
            for plat in self.platforms:
                plat.rect.y += max(abs(self.player.vel.y), 2)
                if plat.rect.top >= HEIGHT:
                    plat.kill()
                    self.score += 10
            for spaw in self.spawns:
                spaw.rect.y += max(abs(self.player.vel.y), 2)
                if spaw.rect.top >= HEIGHT:
                    spaw.kill()
                    self.score += 10
           
        powerhps_hits = pg.sprite.spritecollide(self.player, self.powerhps, True)
        for powhp in powerhps_hits:
            if powhp.type == 'health':
                if self.player.target_health < 100:
                    self.player.target_health += 25
                if self.player.target_health > 100:
                    self.player_target_health = 100
                self.boost_sound.play()

        pow_hits = pg.sprite.spritecollide(self.player, self.powerups, True)
        for pow in pow_hits:
            if pow.type == 'boost':
                self.jump_count += 1
                self.boost_sound.play()
                
        if self.player.rect.bottom > HEIGHT:
            for sprite in self.all_sprites:
                sprite.rect.y -= max(self.player.vel.y, 10)
                if sprite.rect.bottom < 0:
                    sprite.kill()
        if len(self.platforms) == 0:
            self.playing = False

        while len(self.platforms) < 6:
            width = random.randrange(1000, 2500)
            Platform(self, random.randrange(50, WIDTH /2 + 50),
                     random.randrange(-90, -85))

    def events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                if self.playing:
                    self.playing = False
                self.running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    self.player.jump()
                if event.key == pg.K_w:
                    if self.jump_count > 0:
                        self.jump_count -= 1
                        self.player.vel.y = -BOOST_POWER
                        self.jump_sound.play()
                        self.player.jumping = False
                if event.key == pg.K_s:
                    self.pause()
                if event.key == pg.K_i:
                    self.info()
            if event.type == pg.KEYUP:
                if event.key == pg.K_SPACE:
                    self.player.jump_cut()

    def draw(self):
        self.screen.blit(background, background_rect)
        self.all_sprites.draw(self.screen)
        self.draw_text(str(self.score), 22, WIDTH / 2, 15)
        self.draw_text2('-', 22, 56, 550)
        self.draw_text2(str(self.jump_count), 22, 72, 552)
        self.screen.blit(jump_image, (10, 550))
        #self.draw_text2( str(self.player.health), 22, WIDTH /2, 155)
        self.advanced_health()
        pg.display.flip()

    def show_start_screen(self):
        pg.mixer.music.load(path.join(self.snd_dir, 'Loop_The_Old_Tower_Inn.wav'))
        pg.mixer.music.play(loops=-1)
        pg.mixer.music.set_volume(0.5)
        self.screen.blit(start_screen, start_screen_rect)
        self.draw_text(TITLE, 72, WIDTH / 2, 10)
        self.draw_text2("Press any key to play", 22, WIDTH / 2,  540)
        self.draw_text2("High Score: " + str(self.highscore), 22, WIDTH / 2, 70)
        self.draw_text2("Press I for info", 22, WIDTH / 2, 500)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
        
    def show_go_screen(self):
        if not self.running:
            return
        pg.mixer.music.load(path.join(self.snd_dir, 'Loop_The_Old_Tower_Inn.wav'))
        pg.mixer.music.play(loops=-1)
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", 48, WIDTH / 2, HEIGHT / 4)
        self.draw_text2("Score: " + str(self.score), 22, WIDTH / 2, HEIGHT / 2)
        self.draw_text2("Press any key to play again", 22, WIDTH / 2, HEIGHT * 3 / 4)
        if self.score > self.highscore:
            self.highscore = self.score
            self.draw_text("NEW HIGH SCORE!", 22, WIDTH / 2, HEIGHT / 2 + 40)
            with open(path.join(self.dir, HS_FILE), 'w') as f:
                f.write(str(self.score))
        else:
            self.draw_text("High Score: " + str(self.highscore), 22, WIDTH / 2, HEIGHT / 2 + 40)
        pg.display.flip()
        self.wait_for_key()
        pg.mixer.music.fadeout(500)
        pg.mixer.music.set_volume(0.5)

    def wait_for_key(self):
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.running = False
                if event.type == pg.KEYUP:
                    waiting = False
                 
    def draw_text(surf, text, size, x, y):
        font = pg.font.Font('img/OldLondon.ttf', 56)
        text_surface = font.render(text, True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.screen.blit(text_surface, text_rect)
    def draw_text2(surf, text, size, x, y):
        font = pg.font.Font('img/OldLondon.ttf', 36)
        text_surface = font.render(text, True, YELLOW)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.screen.blit(text_surface, text_rect)

g = Game()
g.show_start_screen()
while g.running:
    g.new()
    g.show_go_screen()

pg.quit()