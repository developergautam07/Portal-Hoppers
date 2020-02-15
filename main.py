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
import sys
import random as ra
import time
import pickle
import os
from os import path
from pathlib import Path
from settings import *
from sprites import *
from map import *
from pytmx import *
from DataBridge import *


class Game:
    def __init__(self):
    	# Preinitializing pygame mixer module
        pg.mixer.pre_init(44100, -16, 1, 2048)
        # Intitializing all pygame modules
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.load_data()
        self.Wait_to_start()

    # Function for Fade Transition
    def fade(self):
        f = pg.Surface((WIDTH, HEIGHT))
        f.fill((0, 0, 0))
        for alpha in range(300):
            f.set_alpha(alpha)
            self.screen.fill((255, 255, 255))
            self.screen.blit(f, (0, 0))
            pg.display.update()
            pg.time.delay(2)

    # Function to Draw text
    def draw_text(self, text, fontName, font_size, color, x, y, 
    	align = "center"):
        font = pg.font.Font(fontName, font_size)
        text_renderer = font.render(text, True, color)
        text_rect = text_renderer.get_rect()
        if align == "center":
            text_rect.center = (x, y)
        if align == "topleft":
            text_rect.topleft = (x, y)
        if align == "topright":
            text_rect.topright = (x, y)
        if align == "bottomleft":
            text_rect.bottomleft = (x, y)
        if align == "bottomright":
            text_rect.bottomright = (x, y)
        if align == "midtop":
            text_rect.midtop = (x, y)
        if align == "midright":
            text_rect.midright = (x, y)
        if align == "midleft":
            text_rect.midleft = (x, y)
        if align == "midbottom":
            text_rect.midbottom = (x, y)
        self.screen.blit(text_renderer, text_rect)

    # Function to load game data
    def load_data(self):
        self.dataBridge = data_bridge()
        if not(self.dataBridge.check_tabels()):
            self.dataBridge.database_setup()

        # Loading current level number from database
        self.level = self.dataBridge.get_levels() 

        # Checking the file is frozen or not
        if getattr(sys, 'frozen', False):
            Tiled = path.dirname(sys.executable)
        else:
            Tiled = path.dirname(path.realpath(__file__))
        play_img_fold = path.join(Tiled, "player_sprite")
        self.tiled_map_fold = path.join(Tiled, "Levels")
        bullet_img_fold = path.join(Tiled, "bullet_sprite")
        enemy_img_fold = path.join(Tiled, "enemy_sprite")
        wall_sprite_fold = path.join(Tiled, "wall_sprite")
        flash_fold = path.join(Tiled, "Flash")
        ex_fold = path.join(Tiled, "Damage")
        scr_fold = path.join(Tiled, "Screens")
        SFX_fold = path.join(Tiled, "SFX")
        consumables_fold = path.join(Tiled, "consumables")
        self.bg_music_fold = path.join(Tiled, "music")
        self.font = path.join(Tiled, "Font/seg.ttf")
        self.font_mtB = path.join(Tiled, "Font/Montserrat-Bold.ttf")
        self.play_img = pg.image.load(path.join(play_img_fold, PLAY_IMG)).convert_alpha()
        self.play_img_with_s = pg.image.load(path.join(play_img_fold, PLAY_IMG_S)).convert_alpha()
        self.play_img_idel = pg.image.load(path.join(play_img_fold, PLAY_IMG_IDEL)).convert_alpha()
        self.bullet_imgs = {}
        self.bullet_imgs["L"] = pg.image.load(path.join(bullet_img_fold, BULLET_IMG)).convert_alpha()
        self.bullet_imgs["S"] = pg.transform.scale(self.bullet_imgs["L"], (30, 30))
        self.e_bullet_img = pg.image.load(path.join(bullet_img_fold, BULLET_IMG)).convert_alpha()
        self.enemy_img = pg.image.load(path.join(enemy_img_fold, ENEMY_IMG)).convert_alpha()
        self.boss_img = pg.image.load(path.join(enemy_img_fold, BOSS_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(wall_sprite_fold, WALL_IMG)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.gameover_panel = pg.image.load(path.join(scr_fold, GOV_PANEL)).convert_alpha()
        self.start_screen = pg.image.load(path.join(scr_fold, START_SCREEN)).convert_alpha()
        self.options_screen = pg.image.load(path.join(scr_fold, OPTIONS_SCREEN)).convert_alpha()
        self.load_screen = pg.image.load(path.join(scr_fold, LOAD_SCREEN)).convert_alpha()
        self.mode_screen = pg.image.load(path.join(scr_fold, MODE_SCREEN)).convert_alpha()
        self.pause_screen = pg.image.load(path.join(scr_fold, PAUSE_SCREEN)).convert_alpha()
        self.text_win = pg.image.load(path.join(scr_fold, WINDOW)).convert_alpha()
        self.h_bar_img = pg.image.load(path.join(play_img_fold, H_BAR)).convert_alpha()
        self.robot_rip = pg.image.load(path.join(enemy_img_fold, ENEMY_RIP)).convert_alpha()
        self.robot_rip = pg.transform.scale(self.robot_rip, (64, 64))
        self.pistol_active_img = pg.image.load(path.join(consumables_fold, PISTOL_ACTIVE)).convert_alpha()
        self.shotgun_active_img = pg.image.load(path.join(consumables_fold, SHOTGUN_ACTIVE)).convert_alpha()
        self.weapon_locked_img = pg.image.load(path.join(consumables_fold, WEAPON_LOCKED)).convert_alpha()
        self.enemy_icon = pg.image.load(path.join(enemy_img_fold, ENEMY_ICON)).convert_alpha()
        self.enemy_alert = pg.image.load(path.join(enemy_img_fold, ENEMY_ALERT)).convert_alpha()
        self.enemy_rip_icon = pg.image.load(path.join(enemy_img_fold, ENEMY_RIP_ICON)).convert_alpha()
        self.coming_soon_srn = pg.image.load(path.join(scr_fold, COMMING_SOON)).convert_alpha()
        self.controls_srn = pg.image.load(path.join(scr_fold, CONTROLS_SCREEN)).convert_alpha()
        self.credits_srn = pg.image.load(path.join(scr_fold, CREDITS_SCREEN)).convert_alpha()
        self.splash_srn = pg.image.load(path.join(scr_fold, SPLASH_SCREEN)).convert_alpha()
        
        self.muzzel_flash = []
        for img in MUZZLE_F:
            self.muzzel_flash.append(pg.image.load(path.join(flash_fold, img)).convert_alpha())
        self.ex_effect = []
        for ex in EX:
            self.ex_effect.append(pg.image.load(path.join(ex_fold, ex)).convert_alpha())
        self.consum_img = {}
        for consumables in CONSUMABLE_ITEMS:
            self.consum_img[consumables] = pg.image.load(path.join(consumables_fold, CONSUMABLE_ITEMS[consumables])).convert_alpha()
        pg.display.set_icon(self.consum_img["portal"])
        
        # lighting effect
        self.darkeness = pg.Surface((WIDTH, HEIGHT))
        self.darkeness.fill(DARKGREY)
        self.dark_night = pg.image.load(path.join(scr_fold, DARK_NIGHT)).convert_alpha()
        self.dark_night = pg.transform.scale(self.dark_night, LIGHT_RADIUS)
        self.torch_rect = self.dark_night.get_rect()

        # sound effects
        self.robot_sfx = pg.mixer.Sound(path.join(SFX_fold, ROBOT_SOUND))
        self.pain_sfx = pg.mixer.Sound(path.join(SFX_fold, PAIN_SOUND))
        self.robot_hit = pg.mixer.Sound(path.join(SFX_fold, ROBOT_HIT_SOUND))
        self.explode_sfx = pg.mixer.Sound(path.join(SFX_fold, EXPLODE_SOUND))
        self.start_sfx = pg.mixer.Sound(path.join(SFX_fold, START_SOUND))
        pg.mixer.set_num_channels(10)     # default value is 8

        # weapon sfx
        self.weapon_sfx = {}
        for wp in WEAPON_SOUNDS:
            self.weapon_sfx[wp] = []
            for sfx in WEAPON_SOUNDS[wp]:
                s = pg.mixer.Sound(path.join(SFX_fold, sfx))
                s.set_volume(0.3)
                self.weapon_sfx[wp].append(s)

        #consumable’s sfx
        self.con_sfx = {}
        for con in CON_SOUND:
            self.con_sfx[con] = pg.mixer.Sound(path.join(SFX_fold, CON_SOUND[con]))

    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.e_bullets = pg.sprite.Group()
        self.consumable_items = pg.sprite.Group()
        self.beginning = False
        self.boss_active = False
        self.is_paused = False
        self.started = False
        self.portal_SetActive = False
        self.warn_text = False
        self.dark = False
        self.snow = False
        self.sgun_enabled = False
        self.enemy_active = False
        self.T_text = False
        self.load_level()

    # Function load levels
    def load_level(self):
        if self.level == 1:
            self.Map = Tiled_map(path.join(self.tiled_map_fold, MAP1))
            pg.mixer.music.load(path.join(self.bg_music_fold, BG_MUSIC["level1"]))
            self.map = self.Map.load_map()
        self.map_rect = self.map.get_rect()
        if self.level == 2:
            self.dark = True
            self.Map = Tiled_map(path.join(self.tiled_map_fold, MAP2))
            pg.mixer.music.load(path.join(self.bg_music_fold, BG_MUSIC["level2"]))
            self.map = self.Map.load_map()
        self.map_rect = self.map.get_rect()
        if self.level == 3:
            self.dark = False
            self.snow = True
            self.Map = Tiled_map(path.join(self.tiled_map_fold, MAP3))
            pg.mixer.music.load(path.join(self.bg_music_fold, BG_MUSIC["level3"]))
            self.map = self.Map.load_map()
        self.map_rect = self.map.get_rect()

        # Accessing data tiled map
        for tile_obj in self.Map.tmxdata.objects:
            obj_center = v(tile_obj.x + tile_obj.width/2, tile_obj.y + tile_obj.height/2)
            if tile_obj.name == "player":
                self.player = Player(self, obj_center.x, obj_center.y)
            if tile_obj.name == "robot":
                self.enemy = Enemy(self, obj_center.x, obj_center.y)
            if tile_obj.name == "wall" or "sofa" or "stone" or "tree" or "tv" or "pond":
                Tiled_walls(self, tile_obj.x, tile_obj.y, tile_obj.width, tile_obj.height)
            if tile_obj.name in ["health", "shotgun", "torch"]:
                Consumable(self, obj_center, tile_obj.name)
            if tile_obj.name in ["portal"]:
                Consumable(self, obj_center, tile_obj.name, False)
            if tile_obj.name == "boss" and self.boss_active:
                self.map.blit(self.boss_img, (tile_obj.x, tile_obj.y))

        self.camera = Camera(self.Map.width, self.Map.height)
        #print(self)

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(loops = -1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not (self.is_paused or self.started):
                self.update()
            self.draw()

    def quit(self):
        self.dataBridge.auto_save("", 1, quit = True)
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)
        if len(self.enemies) <= 4 and self.level == 1:
            self.portal_SetActive = True
        distance = self.player.pos - self.enemy.pos

        # player health
        e_bullet_collide_player = pg.sprite.spritecollide(self.player, self.e_bullets, False, collision_with_player)
        for collide in e_bullet_collide_player:
            self.player.Get_Damage()
            pg.mixer.Channel(1).play(self.pain_sfx)
            self.player.armor -= ENEMY_ATTACK
            collide.vel = v(0, 0)
            if self.player.armor <= 0:
                self.player.health -= ENEMY_ATTACK
                collide.vel = v(0, 0)
            if self.player.health <= 0:
                self.Game_Over()
            if e_bullet_collide_player:
                self.player.pos += v(ENEMY_HIT, 0).rotate(-e_bullet_collide_player[0].turn)

        # enemy health
        p_bullet_collide_enemy = pg.sprite.groupcollide(self.enemies, self.bullets, False, True)
        for collide in p_bullet_collide_enemy:
            #self.enemy.E_Get_Damage()
            pg.mixer.Channel(3).play(self.robot_hit)
            collide.life -= WEAPONS[self.player.weapon]["damage"] * len(p_bullet_collide_enemy[collide])
            collide.vel = v(0, 0)

        if self.dataBridge.get_weapones == 2:
            self.sgun_enabled = True

        # Player collides consumables
        player_collide_consumables = pg.sprite.spritecollide(self.player, self.consumable_items, False)
        for collide in player_collide_consumables:
            if collide.type == "health" and self.player.health < PLAYER_HEALTH:
                collide.kill()
                pg.mixer.Channel(2).play(self.con_sfx["pick_health"])
                self.player.increase_health(MEDI_KIT)

            if collide.type == "shotgun":
                collide.kill()
                self.player.weapon = "shotgun"
                self.sgun_enabled = True
                self.dataBridge.auto_save("shotgun", self.level)

            if collide.type == "portal" and (self.portal_SetActive or self.level != 1):
                self.level += 1
                self.dataBridge.auto_save("", self.level)
                self.playing = False
                pg.mixer.music.stop()
                pg.mixer.Channel(5).play(self.con_sfx["portal_sfx"])
                self.fade()
                self.load_level()

            if collide.type == "portal" and not(self.portal_SetActive) and (self.level == 1):
                self.warn_text = True

            if collide.type == "torch" and self.dark:
                collide.kill()
                self.T_text = True

    '''
    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):                                # Horizontal line
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):                               # Vertical line
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    '''

    def render_darkeness(self):
        # drak light gradient on image of darkeness
        self.darkeness.fill(DARKGREY)
        self.torch_rect.center = self.camera.apply(self.player).center
        self.darkeness.blit(self.dark_night, self.torch_rect)
        # Multiply the upper pixel and lower pixel
        self.screen.blit(self.darkeness, (0, 0), special_flags=pg.BLEND_MULT) 

    def draw(self):
        #pg.display.set_caption("{:2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        self.screen.blit(self.map, self.camera.apply_rect(self.map_rect))
        #self.draw_grid()

        keys = pg.key.get_pressed()
        if keys[pg.K_t] and self.T_text:
            self.dark = False
            self.T_text = False
        if keys[pg.K_c] and self.warn_text:
            self.warn_text = False
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.draw_health_bar()
            self.screen.blit(sprite.image, self.camera.apply(sprite))
        #pg.draw.rect(self.screen, WHITE, self.camera.apply(self.player), 2)

        if self.dark:
            self.render_darkeness()

        self.active_weapons()
        if self.T_text:
            self.screen.blit(pg.transform.scale(self.text_win, (WIDTH - 220, HEIGHT - 520)), (WIDTH / 8, HEIGHT - 160))  
            self.draw_text("I Finally got the Torch.", self.font_mtB,  25, WHITE, 330, 590, align = "midbottom")
            self.draw_text("Press T to use the Torch.", self.font_mtB, 25, WHITE, 330, 625, align = "midbottom")

        if self.warn_text:
            self.screen.blit(pg.transform.scale(self.text_win, (WIDTH - 220, HEIGHT - 520)), (WIDTH / 8, HEIGHT - 160))  
            self.draw_text("Wait! I Can't Leave Without Killing Every Single Robot", self.font_mtB, 25, WHITE, 515, 590, align = "midbottom")
            self.draw_text("Press C to continue...", self.font_mtB, 25, WHITE, 300, 625, align = "midbottom")    

        Player.draw_player_healthbar(self.screen, 79, 24, self.player.health / PLAYER_HEALTH)
        Player.draw_player_Aromrbar(self.screen, 79, 63, self.player.armor / ARMOR)
        self.screen.blit(self.h_bar_img, (0, 10))
        if not(self.enemy_active):
            self.screen.blit(self.enemy_icon, (WIDTH - 200, 5))
        if self.enemy_active:
            self.screen.blit(self.enemy_alert, (WIDTH - 200, 5))
        if len(self.enemies) <= 0:
            self.screen.blit(self.enemy_rip_icon, (WIDTH - 200, 5))
        if self.is_paused:
            self.screen.blit(self.pause_screen, (0,0))
        if self.snow:
            self.snowFall()
        pg.display.flip()

    # Weapon locking and unloacking function - Only for display
    def active_weapons(self):
        x = WIDTH // 4
        y = HEIGHT - 130
        if self.player.vel.length_squared() == 0 and not(self.enemy_active) and not(self.warn_text) and not(self.T_text):
            self.screen.blit(self.pistol_active_img, (x, y))  
            #if not(self.sgun_enabled):
            self.weap_locked = self.weapon_locked_img.copy()
            self.screen.blit(self.weap_locked, (x + 150, y))          
            if self.dataBridge.get_weapones() == 2:
                #self.weap_locked.fill((0, 0, 0, 0), special_flags = pg.BLEND_RGBA_MULT)
                self.screen.blit(self.shotgun_active_img, (x + 150, y))
            self.screen.blit(self.weapon_locked_img, (x + 300, y))
        
    def snowFall(self):
        self.gravity = 1
        self.particleSize = 5
        self.numberofParticle = 100
        self.particles = []

        for i in range(self.numberofParticle):
            x = ra.randrange(0,WIDTH)
            y = ra.randrange(0,HEIGHT)
            self.particles.append([x,y])

        for i in self.particles:
            i[1] += self.gravity
            pg.draw.circle(self.screen, WHITE, i, self.particleSize)

            if i[1] > HEIGHT:
                i[1] = ra.randrange(-50,-5)
                i[0] = ra.randrange(WIDTH)
        
    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_paused = not self.is_paused

    def start_menu(self):
        #self.started = not self.started
        self.screen.blit(self.start_screen, (0,0))
        self.New_Btn(373, 278, 280, 70)
        self.Options_Btn = self.Btns(373, 508, 280, 70)
        self.Load_Btn = self.Btns(373, 393, 280, 70)
        #if self.Options_Btn
        pg.display.flip()
        #self.Wait_to_start()
        cur = pg.mouse.get_pos()
        #print(cur)

    def game_over_panel(self):
        self.screen.blit(self.gameover_panel, (0,0))
        self.Retry_Btn(80, 485, 390 ,100)
        self.Quit_Btn(555, 485, 390 ,100)
        pg.display.flip()

    def Btns(self, x, y, w, h):
        cur = pg.mouse.get_pos()
        self.btn_pressed = pg.mouse.get_pressed()
        #print(cur)
        if (x+w > cur[0] > x) and (y+h > cur[1] > y):
            #pg.draw.rect(self.screen, RED, (x, y, w, h),1)
            if self.btn_pressed[0] == 1:
                self.clicked = True
                #print("Clicked")
                return self.clicked

    def New_Btn(self, x, y, w, h):
        cur = pg.mouse.get_pos()
        self.btn_pressed = pg.mouse.get_pressed()
        #print(cur)
        if (x+w > cur[0] > x) and (y+h > cur[1] > y):
            #pg.draw.rect(self.screen, RED, (x, y, w, h),1)
            if self.btn_pressed[0] == 1:
                self.clicked = True
                #print("Clicked")
                return self.clicked

    def Retry_Btn(self, x, y, w, h):
        cur = pg.mouse.get_pos()
        self.btn_pressed = pg.mouse.get_pressed()
        #print(cur)
        if (x+w > cur[0] > x) and (y+h > cur[1] > y):
            #pg.draw.rect(self.screen, RED, (x, y, w, h),1)
            if self.btn_pressed[0] == 1:
                self.clicked = True
                #print("Clicked")
                return self.clicked

    def Quit_Btn(self, x, y, w, h):
        cur = pg.mouse.get_pos()
        self.btn_pressed = pg.mouse.get_pressed()
        #print(cur)
        if (x+w > cur[0] > x) and (y+h > cur[1] > y):
            #pg.draw.rect(self.screen, RED, (x, y, w, h),1)
            if self.btn_pressed[0] == 1:
                self.quit() 

    def options_menu(self):
        self.screen.blit(self.options_screen, (0,0))
        self.Back_Btn = self.Btns(34, 34, 62, 62)
        self.controls_btn = self.Btns(312, 450, 400, 120)
        self.credits_btn = self.Btns(312, 270, 400, 120)
        pg.display.flip()
    
    def load_menu(self):
        self.screen.blit(self.load_screen, (0,0))
        self.Back_Btn = self.Btns(26, 34, 62, 62)
        pg.display.flip()

    def select_mode_menu(self):
        self.screen.blit(self.mode_screen, (0,0))
        self.Back_Btn = self.Btns(26, 34, 62, 62)
        self.story_mode = self.Btns(312, 270, 400, 120)
        self.suvival_mode_btn = self.Btns(312, 450, 400, 120)
        pg.display.flip()

    def comming_soon(self):
        self.screen.blit(self.coming_soon_srn, (0,0))
        self.Back_Btn = self.Btns(26, 34, 62, 62)
        pg.display.flip()
    
    def controls_menu(self):
        self.screen.blit(self.controls_srn, (0,0))
        self.Back_Btn = self.Btns(26, 34, 62, 62)
        pg.display.flip()
    
    def credits_menu(self):
        self.screen.blit(self.credits_srn, (0,0))
        self.Back_Btn = self.Btns(26, 34, 62, 62)
        pg.display.flip()

    def splash_screen(self):
        self.screen.blit(self.splash_srn, (0,0))
        self.Back_Btn = self.Btns(26, 34, 62, 62)
        pg.display.flip()

    def load(self):
        self.playing = False
        while self.Load_Btn:
            self.clock.tick(FPS)
            self.load_menu()
            self.Back_Btn = self.Btns(30, 30, 120 ,100)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.Load_Btn = False
                    self.quit()
                if self.Back_Btn:
                    self.start_menu()
                      
    def options(self):
        #self.Options_Btn = self.Btns(373, 508, 280, 70)
        self.playing = False
        while self.Options_Btn:
            self.clock.tick(FPS)
            self.options_menu()
            self.Back_Btn = self.Btns(30, 30, 120 ,100)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.Options_Btn = False
                    self.quit()
                if self.Back_Btn:
                    self.start_menu()
                if self.controls_btn:
                    self.controls()
                if self.credits_btn:
                    self.credits()

    def credits(self):
        self.playing = False
        while self.credits_btn:
            self.clock.tick(FPS)
            self.credits_menu()
            self.Back_Btn = self.Btns(30, 30, 120 ,100)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.credits_btn = False
                    self.quit()
                if self.Back_Btn:
                    self.credits_btn = False
                    self.options_menu()

    def controls(self):
        self.playing = False
        while self.controls_btn:
            self.clock.tick(FPS)
            self.controls_menu()
            self.Back_Btn = self.Btns(30, 30, 120 ,100)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.controls_btn = False
                    self.quit()
                if self.Back_Btn:
                    self.controls_btn = False
                    self.options_menu()
        
    def survival_mode(self):
        self.playing = False
        while self.suvival_mode_btn:
            self.clock.tick(FPS)
            self.comming_soon()
            self.Back_Btn = self.Btns(30, 30, 120 ,100)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.Options_Btn = False
                    self.quit()
                if self.Back_Btn:
                    self.survival_mode_btn = False
                    self.modes()

    def modes(self):
        #self.Options_Btn = self.Btns(373, 508, 280, 70)
        self.playing = False
        while self.game_mode:
            self.clock.tick(FPS)
            self.select_mode_menu()
            self.Back_Btn = self.Btns(30, 30, 120 ,100)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_mode = False
                    self.quit()
                if self.Back_Btn:
                    self.game_mode = False
                if self.suvival_mode_btn:
                    self.survival_mode()
                if self.story_mode:
                    self.game_mode = False
                    self.waiting = False
                    #self.start_menu()

    def Wait_to_start(self):
        self.waiting = True
        self.playing = False
        self.fade()
        self.splash_screen()
        self.start_sfx.play()
        time.sleep(2)
        self.fade()
        pg.mixer.music.load(path.join(self.bg_music_fold, BG_MUSIC["main_menu"]))
        pg.mixer.music.set_volume(0.3)
        pg.mixer.music.play(loops = -1)
        while self.waiting:
            self.clock.tick(FPS)
            self.start_menu()
            self.game_mode = self.New_Btn(373, 278, 300, 70)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.waiting = False
                    self.quit()
                    #self.running = False
                if self.game_mode:
                    self.modes()
                if self.Options_Btn:
                    self.options()
                    #waiting = False
                if self.Load_Btn:
                    self.load()

    def Game_Over(self):
        pg.event.wait()
        GOV = True
        self.playing = False
        while GOV:
            pg.mixer.music.stop()
            self.clock.tick(FPS)
            self.game_over_panel()
            self.Continue = self.Retry_Btn(80, 485, 390 ,100)
            for event in pg.event.get():
                #print(event)
                if event.type == pg.QUIT:
                    self.quit()
                if self.Continue == True:
                    #self.playing = True
                    self.load_level()
                    GOV = False 
                    

# create the object
g = Game()
#g.start_menu()
while True:
    pg.time.delay(5)
    g.new()
    g.run()
   # g.Game_Over()
