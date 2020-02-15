'''
Portal Hoppers is free software: you can redistribute
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Portal Hoppers is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Portal Hoppers.  If not, see <https://www.gnu.org/licenses/>.
'''
import pygame as pg
from random import uniform, randint, choice, random
from settings import *
import pytweening as anim
from itertools import chain

v = pg.math.Vector2
def collision_with_walls(sprite, group, direc):
    if direc == "x":
        collide = pg.sprite.spritecollide(sprite, group, False, collision_with_player)
        if collide:
            if collide[0].rect.centerx > sprite.collider.centerx:
                sprite.pos.x = collide[0].rect.left - sprite.collider.width /2
            if collide[0].rect.centerx < sprite.collider.centerx:
                sprite.pos.x = collide[0].rect.right + sprite.collider.width /2
            sprite.vel.x = 0;
            sprite.collider.centerx = sprite.pos.x

    if direc == "y":
        collide = pg.sprite.spritecollide(sprite, group, False, collision_with_player)
        if collide:
            if collide[0].rect.centery > sprite.collider.centery:
                sprite.pos.y = collide[0].rect.top - sprite.collider.height /2
            if collide[0].rect.centery < sprite.collider.centery:
                sprite.pos.y = collide[0].rect.bottom + sprite.collider.height /2
            sprite.vel.y = 0;
            sprite.collider.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = PLAYER_LAY
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.play_img
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collider = PLAY_COLLIDER
        self.collider.center = self.rect.center
        self.vel = v(0, 0)
        self.pos = v(x, y)
        self.turn = 0
        self.prev_shot = 0
        self.health = PLAYER_HEALTH
        self.armor = ARMOR
        self.weapon = "pistol"
        self.damage_ef = False


    def get_move_key(self):
        self.turn_vel = 0
        self.vel = v(0, 0)
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.turn_vel = PLAY_TURN_VEL
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.turn_vel = -PLAY_TURN_VEL
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel = v(PLAYER_VEL, 0).rotate(-self.turn)
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel = v(-PLAYER_VEL/2, 0).rotate(-self.turn)
        if keys[pg.K_SPACE] or pg.mouse.get_pressed()[0]:
            self.player_shooting()
        if keys[pg.K_1]:
            self.weapon = "pistol"
        if self.game.dataBridge.get_weapones() == 2 and keys[pg.K_2]:
            self.weapon = "shotgun"

    def player_shooting(self):
        shoot_time = pg.time.get_ticks()
        if shoot_time - self.prev_shot > WEAPONS[self.weapon]["rate"]:
            self.prev_shot = shoot_time
            direc = v(1,0).rotate(-self.turn)
            pos = self.pos + GUN_OFFSET.rotate(-self.turn)
            self.vel = v(-WEAPONS[self.weapon]["pushback"], 0).rotate(-self.turn)
            for i in range(WEAPONS[self.weapon]["n_bullet"]):
                accur = uniform(-WEAPONS[self.weapon]["accuracy"], WEAPONS[self.weapon]["accuracy"])
                Bullet(self.game, pos, direc.rotate(accur))
                w_sfx = choice(self.game.weapon_sfx[self.weapon])   # Selecting weapon fire sund effect
                pg.mixer.Channel(0).play(w_sfx)                            # Playing the weapon sfx
           # Bullet(self.game, pos, direc)
            Muzzel_Flash(self.game, pos)

    def Get_Damage(self):
        self.damage_ef = True
        self.damage_alpha = chain(DAMAGE_ALPHA * 2)

    def update(self):
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.pos += self.vel * self.game.dt
        self.collider.centerx = self.pos.x
        collision_with_walls(self, self.game.walls, "x")
        self.collider.centery = self.pos.y
        collision_with_walls(self, self.game.walls, "y")
        self.rect.center = self.collider.center
        if self.weapon == "shotgun":
            self.image = self.game.play_img_with_s
            self.image = pg.transform.rotate(self.game.play_img_with_s, self.turn)
        self.get_move_key()
        self.turn =(self.turn + self.turn_vel * self.game.dt) % 360
        if self.weapon == "pistol":
            self.image = pg.transform.rotate(self.game.play_img, self.turn)
        if self.game.beginning:
        	self.image = pg.transform.rotate(self.game.play_img_idel, self.turn)
        	self.game.started = True
        if self.damage_ef:
            try:
                self.image.fill((255, 0, 0, next(self.damage_alpha)), special_flags = pg.BLEND_RGBA_MULT)  #special_flags gives the best result of aplha/color/effect quality
            except:
                self.damage_ef = False

    def increase_health(self, amt):
        self.health += amt
        if self.health > PLAYER_HEALTH:
            self.health = PLAYER_HEALTH

    @staticmethod
    def draw_player_healthbar(surf, x, y, healthPer):
         if healthPer < 0:
             healthPer = 0
         BAR_LENGTH = 165
         BAR_HEIGHT = 25
         fill = healthPer * BAR_LENGTH
         #outline = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
         fill_bar = pygame.Rect(x, y, fill, BAR_HEIGHT)
         if healthPer > 0.6:
             color = GREEN
         elif healthPer > 0.35:
             color = YELLOW
         else:
             color = RED
         pygame.draw.rect(surf, color, fill_bar)

    @staticmethod
    def draw_player_Aromrbar(surf, x, y, ArmorPer):
         if ArmorPer < 0:
             ArmorPer = 0
         BAR_LENGTH = 115
         BAR_HEIGHT = 25
         fill = ArmorPer * BAR_LENGTH
         outline = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
         fill_bar = pygame.Rect(x, y, fill, BAR_HEIGHT)
         if ArmorPer > 0.6:
             color = LIGHTGREY
         elif ArmorPer > 0.35:
             color = LIGHTGREY
         else:
             color = LIGHTGREY
         pygame.draw.rect(surf, color, fill_bar)
         #pygame.draw.rect(surf, WHITE, outline, 1)

class Enemy(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = ENEMY_LAY
        self.groups = game.all_sprites, game.enemies
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.enemy_img.copy()
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.collider = ENEMY_COLLIDER.copy()
        self.collider.center = self.rect.center
        self.pos = v(x, y)
        self.vel = v(0,0)
        self.acc = v(0,0)
        self.rect.center = self.pos
        self.turn = 0
        self.life = ENEMY_HEALTH
        self.prev_shot = 0
        self.velocity = choice(ENEMY_VEL)
        self.target = game.player
        self.e_damage_ef = False

    def collision_with_enemy(self):
        return self.rect

    def enemy_shooting(self):
        #if self.vel > 0:
            e_shoot_time = pg.time.get_ticks()
            if e_shoot_time - self.prev_shot > BULLET_RATE * 5:
                self.prev_shot = e_shoot_time
                direc = v(1,0).rotate(-self.turn)
                pos = self.pos + GUN_OFFSET.rotate(-self.turn)
                e_Bullet(self.game, pos, direc)
                self.game.enemy_active = True

    def dist_from_other(self):
        for e in self.game.enemies:
            if e != self:
                dist = self.pos - e.pos
                if 0 < dist.length() < E_DISTANCE:
                    if self.acc != -dist.normalize():
                        self.acc += dist.normalize()
                    else:
                        self.acc += v(choice((self.acc.y, -self.acc.y)), choice((self.acc.x, -self.acc.x)))

    def update(self):
        target_distance = self.target.pos - self.pos
        stop_pos = STOP_RANGE**2
        if target_distance.length_squared() < ENEMY_RANGE**2 and target_distance.length_squared() > stop_pos:
            #if random() < 0.01:
            self.game.robot_sfx.set_volume(0.2)
            self.game.robot_sfx.play()
            self.collision_with_enemy()
            self.enemy_shooting()
            self.turn = target_distance.angle_to(v(1,0))
            self.image = pg.transform.rotate(self.game.enemy_img, self.turn)
            self.rect.center = self.pos
            self.acc = v(1, 0).rotate(-self.turn)
            self.dist_from_other()
            self.acc.scale_to_length(self.velocity)
            self.acc += self.vel * -1
            self.vel += self.acc * self.game.dt
            self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
            self.collider.centerx = self.pos.x
            collision_with_walls(self, self.game.walls, "x")
            self.collider.centery = self.pos.y
            collision_with_walls(self, self.game.walls, "y")
            self.rect.center = self.collider.center
        if target_distance.length_squared() <= stop_pos:
            #self.velocity = 0
            self.turn = target_distance.angle_to(v(1,0))
            self.image = pg.transform.rotate(self.game.enemy_img, self.turn)
            self.enemy_shooting()

        if self.life <= 0:
            pg.mixer.Channel(4).play(self.game.explode_sfx)
            self.kill()
            self.game.enemy_active = False
            explo = Exp(self.game, self.pos)
            self.game.all_sprites.add(explo)
            if (target_distance.length_squared() <= (stop_pos//3)):
                self.game.player.health -= 5
            self.game.map.blit(self.game.robot_rip, self.pos - v(32, 32))
            

    def draw_health_bar(self):
        if self.life > 70:
            color = RED
        elif self.life > 35:
            color = YELLOW
        else:
            color = BLUE
        width = int(self.rect.width * self.life / ENEMY_HEALTH)
        self.health_bar = pg.Rect(0, 0, width, 7)
        if self.life < ENEMY_HEALTH:
            pg.draw.rect(self.image, color, self.health_bar)

class Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, direc):
        self.groups = game.all_sprites, game.bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.bullet_imgs[WEAPONS[game.player.weapon]["b_size"]]
        self.rect = self.image.get_rect()
        self.collider = self.rect
        self.pos = v(pos)
        self.rect.center = pos
        #accur = uniform(-ACCURACY, ACCURACY)
        self.vel = direc * WEAPONS[game.player.weapon]["bullet_vel"] * uniform(0.9, 1.1)
        self.bullet_life = pg.time.get_ticks()
        #self.turn = 0

    def update(self):
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        #self.image = pg.transform.rotate(game.bullet_imgs[WEAPONS[game.player.weapon]["b_size"]], self.turn)
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.bullet_life > WEAPONS[self.game.player.weapon]["bullet_life"] :
            self.kill()

class e_Bullet(pg.sprite.Sprite):
    def __init__(self, game, pos, direc):
        self.groups = game.all_sprites, game.e_bullets
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.e_bullet_img
        self.rect = self.image.get_rect()
        self.collider = self.rect
        self.pos = v(pos)
        self.rect.center = pos
        accur = uniform(-ACCURACY, ACCURACY)
        self.vel = direc.rotate(accur) * BULLET_VEL
        self.bullet_life = pg.time.get_ticks()
        self.turn = 0

    def update(self):
        if pg.sprite.spritecollideany(self, self.game.walls):
            self.kill()
        if pg.time.get_ticks() - self.bullet_life > BULLET_LIFE :
            self.kill()           
        self.pos += self.vel * self.game.dt
        self.rect.center = self.pos
        self.image = pg.transform.rotate(self.game.e_bullet_img, self.turn)
        
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self._layer = WALL_LAY
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        #self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = game.wall_img
        #self.image.fill(BROWN)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Tiled_walls(pg.sprite.Sprite):
    def __init__(self, game, x, y, wid, hei):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, wid, hei)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Muzzel_Flash(pg.sprite.Sprite):
    def __init__(self, game, pos):
        self._layer = EFFECTS_LAY
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = randint(20, 50)
        self.image = pg.transform.scale(choice(game.muzzel_flash), (size, size))
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.center = pos
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        if pg.time.get_ticks() - self.spawn_time > F_DURATION:
            self.kill()

class Exp(pg.sprite.Sprite):
    def __init__(self, game, pos):
        #self._layer = EFFECTS_LAY
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        size = 64
        #self.image = pg.transform.scale(game.ex_effect, (size, size))
        self.image = self.game.ex_effect[0]
        #self.no_of_img = len(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.frame = 0
        self.spawn_time = pg.time.get_ticks()

    def update(self):
        now = pg.time.get_ticks()
        if now - self.spawn_time > F_DURATION:
            self.spawn_time += 1
            self.frame += 1
            if self.frame == len(EX):
                self.kill()
            else:
                center = self.rect.center
                self.image = self.game.ex_effect[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

class Consumable(pg.sprite.Sprite):
    def __init__(self, game, pos, type, is_anime = True):
        self._layer = CONSUME_LAY
        self.groups = game.all_sprites, game.consumable_items
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.is_anime = is_anime
        self.image = game.consum_img[type]
        self.rect = self.image.get_rect()
        self.type = type
        self.pos = pos
        self.rect.center = pos
        if self.is_anime:
            self.anim = anim.easeInQuart
        self.step = 0
        self.dirc = 1

    def update(self):
        if self.is_anime:
            offset = ANIM_RANGE * (self.anim(self.step / ANIM_RANGE) - 0.5)
            self.rect.centery = self.pos.y + offset * self.dirc
            self.step += ANIM_SPEED
            if self.step > ANIM_RANGE:
                self.step = 0
                self.dirc *= -1
