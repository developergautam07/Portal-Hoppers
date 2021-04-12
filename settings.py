import pygame
import random as ra
from DataBridge import * 
v = pygame.math.Vector2

# Colours in (R, G, B) -------------------------------------------- #   
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (20, 20, 20)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 225)
YELLOW = (255, 255, 0)
DARKGREEN = (31, 111, 23)
BROWN = (106, 55, 5)
SKIN = (243, 185, 122)

# Game settings --------------------------------------------------- #
WIDTH = 1024
HEIGHT = 670
FPS = 60
TITLE = "Portal Hopper"
BGCOLOR = DARKGREEN
TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

# Player ---------------------------------------------------------- # 
PLAYER = 100
PLAYER_HEALTH = 100
PLAYER_VEL = 4
PLAY_TURN_VEL = 5
PLAY_IMG = "Survivor 1/survivor1_silencer.png"
PLAY_IMG_S = "Survivor 1/survivor1_gun.png"
PLAY_IMG_IDEL = "Survivor 1/survivor1_hold.png"
H_BAR = "hbar.png"
PLAY_COLLIDER = pygame.Rect(0, 0, 32, 32)
LIGHT_RADIUS = (400, 400)
ARMOR = 70
CURRENT_SCENE = 1
db = data_bridge()
PLAYER_NAME = db.get_name() #Review THis
print("From Settings", PLAYER_NAME)
# Collider rect for player
collision_with_player = lambda a, b : a.collider.colliderect(b.rect)

# Enemies --------------------------------------------------------- # 
ENEMY_IMG = "Robot 1/robot1_gun.png"
BOSS_IMG = "Hitman 1/hitman1_machine.png"
ENEMY_RIP = "rip.png"
ENEMY_ICON = "Robot1.png"
ENEMY_ALERT = "Robot_Alert.png"
ENEMY_RIP_ICON = "Robot_Rip_icon.png"
ENEMY_VEL = [250, 200, 150, 100]
ENEMY_COLLIDER = pygame.Rect(0, 0, 32, 32)
ENEMY_HEALTH = 100
ENEMY_ATTACK = ra.randint(1,3)
print(ENEMY_ATTACK)
ENEMY_HIT = 5
E_DISTANCE = 70   # Distance from each enemy in px
ENEMY_RANGE = 400
STOP_RANGE = 200

# Obstacls --------------------------------------------------------- #  
WALL_IMG = "tile_71.png"


# Weapon settings -------------------------------------------------- #
BULLET_IMG = "bullets.png"
GUN_OFFSET = v(30, 10)

# Weapon settings for player --------------------------------------- #
ACTIVE_WEAPONS = 1
WEAPONS = {}
# bullet life (in seconds) = range of the weapon
WEAPONS["pistol"] = {"bullet_vel":500, "bullet_life": 700, "rate": 500, "pushback": 1, "accuracy": 1, "damage": 10, "b_size": "L", "n_bullet": 1}

WEAPONS["shotgun"] = {"bullet_vel":400, "bullet_life": 300, "rate": 900, "pushback": 5, "accuracy": 20, "damage": 7, "b_size": "S", "n_bullet": 8}

# Pistol Active/unlocked image
PISTOL_ACTIVE = "pistol_active.png"
# Shotgun Active/unlocked image 
SHOTGUN_ACTIVE = "shotgun_active.png"
# weapon locked image
WEAPON_LOCKED = "weapon_lock.png"

# Weapon settings for enemies -------------------------------------- #
PUSHBACK = 25
BULLET_VEL = 500
BULLET_LIFE = 280   # 1 sec = 1000 milli sec
BULLET_RATE = 150
ACCURACY = 5
DAMAGE = 50

# SFX -------------------------------------------------------------- # 
WEAPON_SOUNDS = {"pistol" : ["pistol.wav"], "shotgun" :["shotgun.wav"]}
CON_SOUND = {"pick_health":"pick-up-health.wav","portal_sfx":"portal_sound.wav"}
PAIN_SOUND = "pain-3.wav"
ROBOT_SOUND = "robot_alert.wav"
ROBOT_HIT_SOUND = "robot_hit.wav"
EXPLODE_SOUND = "explode.wav"
START_SOUND = "ph_snd.wav"
BG_MUSIC = {"level1" : "l1.wav", "level2" : "l2.wav", "level3" : "l3.wav",
 "main_menu" : "mm.wav"}

#VFX -------------------------------------------------------------- # 

# Muzzle Flash imgs
MUZZLE_F = ["flash0{}.png".format(i) for i in range(9)]
F_DURATION = 40

# Explosion
EX = ["Ve000{}.png".format(i) for i in range(10)] + ["Ve00{}.png".format(i) for i in range (10, 64)]  

# Damage effect
DAMAGE_ALPHA = [i for i in range(0, 255, 25)]

# Maps ------------------------------------------------------------ #        
MAP1 = "level_1.tmx"
MAP2 = "level 2.tmx"
MAP3 = "level 3.tmx"
DARK_NIGHT = "light_350_soft.png"

# Layers (Not work with TiledMapEditor)---------------------------- # 
CONSUME_LAY = 1
WALL_LAY = 3
PLAYER_LAY = 2
ENEMY_LAY = 2
EFFECTS_LAY = 4


# Consumables ----------------------------------------------------- #      
CONSUMABLE_ITEMS = {"health" : "medikit.png", "portal" : "portal.png", 
   "shotgun" : "shotgun.png", "torch" : "torch.png"}
MEDI_KIT = 20
ANIM_RANGE = 20
ANIM_SPEED = 0.7

# Menu Images ----------------------------------------------------- #       

# Game_over_panel image
GOV_PANEL = "game over screen.png"
 
# Start Screen image
START_SCREEN = "start screen.png"

# Options Screen image
OPTIONS_SCREEN = "options screen.png"

# Load Screen image
LOAD_SCREEN = "load screen.png"

# Select Game Mode Screen image
MODE_SCREEN = "new game screen.png"

WINDOW = "nwindo.png"

# Comming soon screen image
COMMING_SOON = "coming soon screen.png"

# Controls Screen image
CONTROLS_SCREEN = "controls screen.png"

# Credit Screen image
CREDITS_SCREEN = 'credits screen.png'

# Splash Screen image
SPLASH_SCREEN = 'title.png'

# Pause screen image
PAUSE_SCREEN = "pause.jpg"

TUT1 = 'tut1.png'

TUT2 = 'tut2.png'
