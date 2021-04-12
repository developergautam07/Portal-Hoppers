import pygame as pg
import ptext
import sys
from settings import *
from DataBridge import *

class T_Animation:
    """Class for text animation"""

    def __init__(self, game, window, clock, bg):
        self.window = window
        self.clock = clock
        self.bg = bg
        self.game = game

    def animate_text(self, text_to_animate, font, x, y, color, size=32):
        '''Main loop for animation'''

        #pg.init()
        self.TextColor = color
        # Triple quoted strings contain newline characters.
        self.text_orig = text_to_animate

        # Create an iterator so that we can get one character after the other.
        text_iterator = iter(self.text_orig)
        text = ''
        
        db = data_bridge()
        self.player_name = db.get_name()

        if self.game.dark:
            self.game.render_darkeness()

        self.game.screen.blit(pg.transform.scale(self.game.text_win, (WIDTH - 200, HEIGHT - 425)), (WIDTH / 8, HEIGHT - 250))
        self.game.draw_text(f"{self.player_name}", self.game.font_mtB, 42, WHITE, (WIDTH / 3) + 140, HEIGHT - 190)

        i = 0  # End position of the string.
        done = False
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                    pg.quit()
                    sys.exit()
                # Press 'r' to reset the text.
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        text_iterator = iter(self.text_orig)
                        text = ''
                    if (event.key == pg.K_t) and self.game.T_text:
                        self.game.T_text = False
                        self.game.dark = False
                        done = True
                    if (event.key == pg.K_c) and self.game.warn_text:
                        self.game.player.vel = v(-(PLAYER_VEL+100), 0).rotate(-self.game.player.angle)
                        self.game.warn_text = False
                        done = True

            if len(text) < len(self.text_orig):
                # Call `next(text_iterator)` to get the next character,
                # then concatenate it with the text.
                text += next(text_iterator)

            i += 1.5  # You can control the speed here.     

            #self.window.blit(self.bg, (x, y))
            ptext.draw(self.text_orig[:int(i)], (x, y), color=self.TextColor, fontname=font, fontsize=size)
            pg.display.flip()
            self.clock.tick(60)


# Uncomment the below lines to run

'''
tta = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
        eiusmod tempor incididunt ut labore et dolore magna aliqua.

        Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris
        nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in
        reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
        pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
        culpa qui officia deserunt mollit anim id est laborum."""
t = T_Animation() 
t.animate_text(tta)
'''