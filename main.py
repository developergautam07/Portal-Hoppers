# Setup Python --------------------------------------------------- #
import pygame as pg
import sys
import random as ra
#import os
from os import path
from settings import *
from sprites import *
from map import *
from pytmx import *
from DataBridge import *
from anime_text import *


class Game:
    # Initializing & Loading Game Data ---------------------------- #
    def __init__(self):
        # Preinitializing pygame mixer module
        pg.mixer.pre_init(44100, -16, 1, 2048)
        # Intitializing all pygame modules
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(500, 100)
        self.timer = 0
        self.load_data()
        self.Wait_to_start()

    def load_img(self, fname, iname):
        img = pg.image.load(path.join(fname, iname)).convert_alpha()
        return img

    def load_data(self):
        '''Function to load game data'''
        self.dataBridge = data_bridge()
        if not(self.dataBridge.check_tabels()):
            self.dataBridge.database_setup()
        else:
            self.game_isloded = True

        # Loading current level number from database
        #self.level = 1

        # Checking the file is frozen or not
        if getattr(sys, 'frozen', False):
            Tiled = path.dirname(sys.executable)
        else:
            Tiled = path.dirname(path.realpath(__file__))
        
        # Folders ------------------------------------------------- #  
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

        # Fonts --------------------------------------------------- # 
        self.font = path.join(Tiled, "Font/seg.ttf")
        self.font_mtB = path.join(Tiled, "Font/Montserrat-Bold.ttf")
        
        # Images -------------------------------------------------- # 
        self.play_img = self.load_img(play_img_fold, PLAY_IMG)
        self.play_img_with_s = self.load_img(play_img_fold, PLAY_IMG_S)
        self.play_img_idel = self.load_img(play_img_fold, PLAY_IMG_IDEL)
        self.bullet_imgs = {}
        self.bullet_imgs["L"] = self.load_img(bullet_img_fold, BULLET_IMG)
        self.bullet_imgs["S"] = pg.transform.scale(self.bullet_imgs["L"], (30, 30))
        self.e_bullet_img = self.load_img(bullet_img_fold, BULLET_IMG)
        self.enemy_img = self.load_img(enemy_img_fold, ENEMY_IMG)
        self.boss_img = self.load_img(enemy_img_fold, BOSS_IMG)
        self.wall_img = self.load_img(wall_sprite_fold, WALL_IMG)
        self.wall_img = pg.transform.scale(self.wall_img, (TILESIZE, TILESIZE))
        self.gameover_panel = self.load_img(scr_fold, GOV_PANEL)
        self.start_screen = self.load_img(scr_fold, START_SCREEN)
        self.options_screen = self.load_img(scr_fold, OPTIONS_SCREEN)
        self.load_screen = self.load_img(scr_fold, LOAD_SCREEN)
        self.mode_screen = self.load_img(scr_fold, MODE_SCREEN)
        self.pause_screen = self.load_img(scr_fold, PAUSE_SCREEN)
        self.text_win = self.load_img(scr_fold, WINDOW)
        self.tut1_img = self.load_img(scr_fold, TUT1)
        self.tut2_img = self.load_img(scr_fold, TUT2)
        self.h_bar_img = self.load_img(play_img_fold, H_BAR)
        self.robot_rip = self.load_img(enemy_img_fold, ENEMY_RIP)
        self.robot_rip = pg.transform.scale(self.robot_rip, (64, 64))
        self.pistol_active_img = self.load_img(consumables_fold, PISTOL_ACTIVE)
        self.shotgun_active_img = self.load_img(consumables_fold, SHOTGUN_ACTIVE)
        self.weapon_locked_img = self.load_img(consumables_fold, WEAPON_LOCKED)
        self.enemy_icon = self.load_img(enemy_img_fold, ENEMY_ICON)
        self.enemy_alert = self.load_img(enemy_img_fold, ENEMY_ALERT)
        self.enemy_rip_icon = self.load_img(enemy_img_fold, ENEMY_RIP_ICON)
        self.coming_soon_srn = self.load_img(scr_fold, COMMING_SOON)
        self.controls_srn = self.load_img(scr_fold, CONTROLS_SCREEN)
        self.credits_srn = self.load_img(scr_fold, CREDITS_SCREEN)
        self.splash_srn = self.load_img(scr_fold, SPLASH_SCREEN)
        
        self.muzzel_flash = []
        for img in MUZZLE_F:
            self.muzzel_flash.append(self.load_img(flash_fold, img))
        self.ex_effect = []
        for ex in EX:
            self.ex_effect.append(self.load_img(ex_fold, ex))
        self.consum_img = {}
        for consumables in CONSUMABLE_ITEMS:
            self.consum_img[consumables] = self.load_img(consumables_fold, CONSUMABLE_ITEMS[consumables])
        
        # icon ---------------------------------------------------- # 
        pg.display.set_icon(self.consum_img["portal"])
        
        # lighting effect ----------------------------------------- #       
        self.darkeness = pg.Surface((WIDTH, HEIGHT))
        self.darkeness.fill(DARKGREY)
        self.dark_night = pg.image.load(path.join(scr_fold, DARK_NIGHT)).convert_alpha()
        self.dark_night = pg.transform.scale(self.dark_night, LIGHT_RADIUS)
        self.torch_rect = self.dark_night.get_rect()

        # sound effects ------------------------------------------- #
        self.robot_sfx = pg.mixer.Sound(path.join(SFX_fold, ROBOT_SOUND))
        self.pain_sfx = pg.mixer.Sound(path.join(SFX_fold, PAIN_SOUND))
        self.robot_hit = pg.mixer.Sound(path.join(SFX_fold, ROBOT_HIT_SOUND))
        self.explode_sfx = pg.mixer.Sound(path.join(SFX_fold, EXPLODE_SOUND))
        self.start_sfx = pg.mixer.Sound(path.join(SFX_fold, START_SOUND))
        pg.mixer.set_num_channels(10)     # default value is 8

        # weapon sfx ---------------------------------------------- #
        self.weapon_sfx = {}
        for wp in WEAPON_SOUNDS:
            self.weapon_sfx[wp] = []
            for sfx in WEAPON_SOUNDS[wp]:
                s = pg.mixer.Sound(path.join(SFX_fold, sfx))
                s.set_volume(0.3)
                self.weapon_sfx[wp].append(s)

        #consumable’s sfx ----------------------------------------- #
        self.con_sfx = {}
        for con in CON_SOUND:
            self.con_sfx[con] = pg.mixer.Sound(path.join(SFX_fold, CON_SOUND[con]))

    def new(self):
        '''initialize all variables and do all the setup for a new game'''
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.e_bullets = pg.sprite.Group()
        self.consumable_items = pg.sprite.Group()
        self.tut = False # Show tutorial
        self.beginning = False  # Starting Cut scene on off switch
        self.boss_active = False # Boss sprite activation switch
        self.game_isloded = False # Switch for load game
        self.is_paused = False # Pause switch
        self.started = False # Checks game started or not
        self.portal_SetActive = False # Portal activation switch
        self.warn_text = False # Level 1 dialouge switch
        self.dark = False # Switch for dark/night mode
        self.snow = False # Switch for snow fall
        self.sgun_enabled = False # Switch enable/disable shotgun
        self.enemy_active = False # Enemy Alert Switch
        self.T_text = False # Level 2 dialouge switch
        self.load_level() # Calling load level function

    def load_level(self):
        '''Function to load levels'''
        if self.level == 1:
            self.Map = Tiled_map(path.join(self.tiled_map_fold, MAP1))
            pg.mixer.music.load(path.join(self.bg_music_fold, BG_MUSIC["level1"]))
            self.map = self.Map.load_map()
            self.map_rect = self.map.get_rect()
        if self.level == 2:
            self.dark = True
            #self.T_text = False
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
            
            if tile_obj.name in ["health", "torch"]:
                Consumable(self, obj_center, tile_obj.name)
            if tile_obj.name in ["shotgun"] and self.dataBridge.get_weapones() < 2:
                Consumable(self, obj_center, tile_obj.name)
            if tile_obj.name in ["portal"]:
                Consumable(self, obj_center, tile_obj.name, False)
            if tile_obj.name == "boss" and self.boss_active:
                self.map.blit(self.boss_img, (tile_obj.x, tile_obj.y))

        self.camera = Camera(self.Map.width, self.Map.height)
        #self.get_pname()
        self.draw_AText = T_Animation(self, self.screen, self.clock, self.text_win)

    #This function is currently not in use
    def get_pname(self):
        '''function to read player name from data file'''
        p_data = {}
        global PLAYER_NAME
        try:
            with open('playerdata.txt', 'r') as f_obj:
                p_data = eval(f_obj.readline())
                PLAYER_NAME = p_data['playername']
        except:
            PLAYER_NAME = 'Player'

    # Updating & Drawing ------------------------------------------ #

    def update(self):
        '''update portion of the game loop'''
        self.all_sprites.update()
        self.camera.update(self.player)
        if len(self.enemies) == 0 and self.level == 1:
            self.portal_SetActive = True

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
                self.dataBridge.auto_save("shotgun", self.level, pl_name=PLAYER_NAME)

            if collide.type == "portal" and (self.portal_SetActive or self.level != 1):
                self.level += 1
                self.dataBridge.auto_save("", self.level, PLAYER_NAME)
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

    def draw(self):
        '''function to draw/display anything on game'''

        # Map ----------------------------------------------------- #       
        self.screen.blit(self.map, self.camera.apply_rect(self.map_rect))
        

        # Dialouges & Tutorials ----------------------------------- #
        if self.warn_text: 
            self.draw_AText.animate_text("Wait! I Can't Leave Without Killing \nEvery Single Robot ! \nPress C to continue...", self.font_mtB, (WIDTH / 3) + 50, HEIGHT - 120, SKIN, size=26) 

        if self.T_text:
            self.draw_AText.animate_text("I Finally got the Torch \nPress T to use the Torch...", self.font_mtB, (WIDTH / 3) + 50, HEIGHT - 120, SKIN, size=26)

        if self.level == 1:
            if not self.tut:
                self.timer = (self.timer + 1) % 50
                if self.timer <= 42:
                    self.screen.blit(self.tut1_img, (WIDTH//2, HEIGHT//8))
                else:
                    self.screen.blit(self.tut2_img, (WIDTH//2, HEIGHT//8))

        # Enemy Images -------------------------------------------- #
        if len(self.enemies) <= 0:
            self.screen.blit(self.enemy_rip_icon, (WIDTH - 200, 5))
        for sprite in self.all_sprites:
            if isinstance(sprite, Enemy):
                sprite.draw_health_bar()
                #pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(sprite.collider), 2)
            self.screen.blit(sprite.image, self.camera.apply(sprite))

        # Other --------------------------------------------------- #      
        # Activate Dark/Night Mode
        if self.dark:
            self.render_darkeness()
 
        # Activate SnowFall
        if self.snow:
            self.snowFall()
        
        # Weapon Locks
        self.active_weapons()

        # Images
        if not(self.enemy_active):
            self.screen.blit(self.enemy_icon, (WIDTH - 200, 5))
        if self.enemy_active:
            self.screen.blit(self.enemy_alert, (WIDTH - 200, 5))

        # Player Health Bar
        Player.draw_player_healthbar(self.screen, 79, 24, self.player.health / PLAYER_HEALTH)
        Player.draw_player_Aromrbar(self.screen, 79, 63, self.player.armor / ARMOR)
        self.screen.blit(self.h_bar_img, (0, 10))


        # Show Pause Screen
        if self.is_paused:
            self.screen.blit(self.pause_screen, (0,0))
        

        #pg.draw.rect(self.screen, WHITE, self.camera.apply_rect(self.player.collider), 2)
        pg.display.flip()

    def render_darkeness(self):
        '''Function to enable dark mode'''
        
        # Drak light gradient on image of darkeness
        self.darkeness.fill(DARKGREY)
        self.torch_rect.center = self.camera.apply(self.player).center
        self.darkeness.blit(self.dark_night, self.torch_rect)
        self.screen.blit(self.darkeness, (0, 0), special_flags=pg.BLEND_MULT)
        # Flag multiplies the upper pixel and lower pixel 

    def draw_text(self, text, fontName, font_size, color, x, y, 
        align = "center"):
        '''Function to Draw text'''
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

    def fade(self):
        ''' Function for fade transistion effect'''
        f = pg.Surface((WIDTH, HEIGHT))
        f.fill((0, 0, 0))
        for alpha in range(300):
            f.set_alpha(alpha)
            self.screen.fill((255, 255, 255))
            self.screen.blit(f, (0, 0))
            pg.display.update()
            pg.time.delay(2)

    def active_weapons(self):
        '''Weapon locking and unloacking function - Only for display'''
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
        '''Function for snowfall'''
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

    # Buttons ----------------------------------------------------- #       

    def Btns(self, x, y, w, h):
        '''Function to make button'''
        cur = pg.mouse.get_pos()
        self.btn_pressed = pg.mouse.get_pressed()
        #print(cur)
        if (x+w > cur[0] > x) and (y+h > cur[1] > y):
            pg.draw.rect(self.screen, RED, (x, y, w, h),1)
            if self.btn_pressed[0] == 1:
                self.clicked = True
                #print("Clicked")
                return self.clicked

    def New_Btn(self, x, y, w, h):
        '''function to make new button'''
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
        '''function for retry'''
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
        '''function for quit button'''
        cur = pg.mouse.get_pos()
        self.btn_pressed = pg.mouse.get_pressed()
        #print(cur)
        if (x+w > cur[0] > x) and (y+h > cur[1] > y):
            #pg.draw.rect(self.screen, RED, (x, y, w, h),1)
            if self.btn_pressed[0] == 1:
                self.quit() 

    # Game Menus -------------------------------------------------- #

    def comming_soon(self):
        '''function to draw comming soon screen'''
        self.screen.blit(self.coming_soon_srn, (0,0))
        self.Back_Btn = self.Btns(26, 34, 62, 62)
        pg.display.flip()

    def load_menu(self):
        '''function to draw load menu'''
        self.screen.blit(self.load_screen, (0,0))
        self.Back_Btn = self.Btns(26, 34, 62, 62)
        self.Load_GameBtn = self.Btns((WIDTH/3) - 25, (HEIGHT/2) - 75, 400 ,100)
        pg.display.flip()

    def load(self):
        '''main loop for load menu'''
        self.playing = False
        while self.Load_Btn:
            self.clock.tick(FPS)
            self.load_menu()
            self.Back_Btn = self.Btns(26, 34, 62, 62)
            self.Load_GameBtn = self.Btns((WIDTH/3) - 25, (HEIGHT/2) - 75, 400 ,100)
            if self.game_isloded:
                self.draw_text(f'{self.dataBridge.get_time()}', self.font_mtB, 32, WHITE, WIDTH//2, (HEIGHT//2) - 25 )
                #pg.display.flip()
                self.draw_text('EMPTY', self.font_mtB, 32, WHITE, WIDTH//2, (HEIGHT//2) + 175 )
                pg.display.flip()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.Load_Btn = False
                    self.quit()
                if self.Back_Btn:
                    self.start_menu()
                if self.Load_GameBtn:
                    self.level = self.dataBridge.get_levels() 
                    self.Load_GameBtn = False
                    self.Load_Btn = False 
                    self.waiting = False
                      
    def options_menu(self):
        '''function to draw options menu'''
        self.screen.blit(self.options_screen, (0,0))
        self.Back_Btn = self.Btns(34, 34, 62, 62)
        self.controls_btn = self.Btns(312, 450, 400, 120)
        self.credits_btn = self.Btns(312, 270, 400, 120)
        pg.display.flip()

    def options(self):
        '''main loop for options menu'''
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

    def credits_menu(self):
        '''function to draw credits menu'''
        self.screen.blit(self.credits_srn, (0,0))
        self.Back_Btn = self.Btns(26, 34, 62, 62)
        pg.display.flip()

    def credits(self):
        '''main loop for credits menu'''
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

    def controls_menu(self):
        '''function to draw controls menu'''
        self.screen.blit(self.controls_srn, (0,0))
        self.Back_Btn = self.Btns(26, 34, 62, 62)
        pg.display.flip()

    def controls(self):
        '''main loop for controls menu'''
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
        '''main loop for survival mode menu'''
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

    def select_mode_menu(self):
        '''This function is to draw the select mode menu'''
        self.screen.blit(self.mode_screen, (0,0))
        self.Back_Btn = self.Btns(26, 34, 62, 62)
        self.story_mode = self.Btns(312, 270, 400, 120)
        self.suvival_mode_btn = self.Btns(312, 450, 400, 120)
        pg.display.flip()

    def modes(self):
        '''main loop for select mode menu'''
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
                	self.level = 1
                	self.dataBridge.update_name('Player', start = True)
                	self.game_mode = False
                	self.waiting = False
                    #self.start_menu()

    def game_over_panel(self):
        '''This function is to draw the gov panel'''
        self.screen.blit(self.gameover_panel, (0,0))
        self.Retry_Btn(80, 485, 390 ,100)
        self.Quit_Btn(555, 485, 390 ,100)
        pg.display.flip()

    def Game_Over(self):
        '''main loop for gov'''
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

    def splash_screen(self):
        '''function to draw splash screen'''
        self.screen.blit(self.splash_srn, (0,0))
        self.Back_Btn = self.Btns(26, 34, 62, 62)
        pg.display.flip()

    def start_menu(self):
        '''function to draw main menu'''
        #self.started = not self.started
        self.screen.blit(self.start_screen, (0,0))
        self.New_Btn(373, 278, 280, 70)
        self.Options_Btn = self.Btns(373, 508, 280, 70)
        self.Load_Btn = self.Btns(373, 393, 280, 70)
        #if self.Options_Btn
        pg.display.flip()
        #self.Wait_to_start()
        #cur = pg.mouse.get_pos()
        #print(cur)

    def Wait_to_start(self):
        '''main loop for main menu''' 
        self.waiting = True
        self.playing = False
        #self.fade()
        #self.splash_screen()
        #self.start_sfx.play()
        #time.sleep(2)
        #aself.fade()
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

    # Others ------------------------------------------------------ #   

    def events(self):
        '''catch all events here'''
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.is_paused = not self.is_paused

    def run(self):
        # game loop - set self.playing = False to end the game
        #self.get_pname()
        PLAYER_NAME = self.dataBridge.get_name()
        if self.level <= 1 and PLAYER_NAME == 'Player':
            import get_name
            #gn.SaveName()
            #self.started = True
            #self.boss_active = True
        self.playing = True
        #self.get_pname()
        PLAYER_NAME = self.dataBridge.get_name()
        self.p_name = PLAYER_NAME
        print(PLAYER_NAME)
        pg.mixer.music.set_volume(0.2)
        pg.mixer.music.play(loops = -1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            self.draw()
            if not (self.is_paused or self.started):
                self.update()

    def quit(self):
        '''funtion to quit game'''
        PLAYER_NAME = self.dataBridge.get_name()
        self.dataBridge.auto_save("", self.level, PLAYER_NAME)
        pg.quit()
        sys.exit()
                    
g = Game() # Create the object for Game

# Main Game Loop -------------------------------------------------- #       
while True:
    pg.time.delay(1)
    g.new()
    g.run()
    