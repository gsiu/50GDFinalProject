import pygame, sys, random, time, cPickle, operator
from pygame.locals import *
from random import *
from operator import itemgetter



from title import *
from game import *
from highscores import *

try:
    import android
except ImportError:
    android = None

try: 
    import pygame.mixer as mixer    
except ImportError:
    import android.mixer as mixer

if android:
    android.init()

def main():
    # Check if sound and font are supported
    if not pygame.font:
        print "Warning, fonts disabled"
   
    
    # Constants
    FPS = 35
    SCREEN_WIDTH, SCREEN_HEIGHT = 480, 800
    SCREENRECT = Rect(0, 0, 480, 800)
    SPEED = 5
    BACKGROUND_COLOR = (0, 0, 0)
    
   # font = pygame.font.Font(None, 30)
    
    score = 0

    levelNum = 0

    # Initialize Pygame, the clock (for FPS), and a simple counter
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 0) 
    pygame.display.set_caption('Sky High')
    clock = pygame.time.Clock()
    
    # Game loop
    while True:
        time_passed = clock.tick(FPS)
        
        if levelNum == 0:
            levelNum = title(screen)
            # Returns 99 if "Play Game" is clicked, 100 if "View Highscores" is clicked

        elif levelNum == 100:
            levelNum = scores(screen)
            # Returns 0 when player exits highscore screen
            levelNum = 0

        else: # levelNum == 99:
            t = game(screen)
            score = score + int(t)
            if android:
                filename = "highscores.txt"
            else:
                filename = "highscores.txt" 
            highscore = [("",0), ("",0), ("",0), ("",0), ("",0), ("",0), ("",0), ("",0)]
            try: # If there is already a highscores file, try opening it
                f = open(filename, "r+")
            except IOError: # If there is no highscores file, create one and add 0's to it
                f = open(filename, "w+")
                cPickle.dump(highscore, f)
                f.seek(0)
            try:
  
                highscore = cPickle.load(f)
                
            except EOFError:
                    pass # Just don't load anything
            username = "Anonymous"
            if android:
##                android.show_keyboard()
##
##                #KEY MAPPING
##                android.map_key(android.KEYCODE_BACK, pygame.K_BACKSPACE)
##                android.map_key(android.KEYCODE_ENTER, pygame.K_RETURN)
##                android.map_key(android.KEYCODE_SPACE, pygame.K_SPACE)
##                android.map_key(android.KEYCODE_A, pygame.K_a)
##                android.map_key(android.KEYCODE_B, pygame.K_b)
##                android.map_key(android.KEYCODE_C, pygame.K_c)
##                android.map_key(android.KEYCODE_D, pygame.K_d)
##                android.map_key(android.KEYCODE_E, pygame.K_e)
##                android.map_key(android.KEYCODE_F, pygame.K_f)
##                android.map_key(android.KEYCODE_G, pygame.K_g)
##                android.map_key(android.KEYCODE_H, pygame.K_h)
##                android.map_key(android.KEYCODE_I, pygame.K_i)
##                android.map_key(android.KEYCODE_J, pygame.K_j)
##                android.map_key(android.KEYCODE_K, pygame.K_k)
##                android.map_key(android.KEYCODE_L, pygame.K_l)
##                android.map_key(android.KEYCODE_M, pygame.K_m)
##                android.map_key(android.KEYCODE_N, pygame.K_n)
##                android.map_key(android.KEYCODE_O, pygame.K_o)
##                android.map_key(android.KEYCODE_P, pygame.K_p)
##                android.map_key(android.KEYCODE_Q, pygame.K_q)
##                android.map_key(android.KEYCODE_R, pygame.K_r)
##                android.map_key(android.KEYCODE_S, pygame.K_s)
##                android.map_key(android.KEYCODE_T, pygame.K_t)
##                android.map_key(android.KEYCODE_U, pygame.K_u)
##                android.map_key(android.KEYCODE_V, pygame.K_v)
##                android.map_key(android.KEYCODE_W, pygame.K_w)
##                android.map_key(android.KEYCODE_X, pygame.K_x)
##                android.map_key(android.KEYCODE_Y, pygame.K_y)
##                android.map_key(android.KEYCODE_Z, pygame.K_z)
##                android.map_key(android.KEYCODE_0, pygame.K_0)
##                android.map_key(android.KEYCODE_1, pygame.K_1)
##                android.map_key(android.KEYCODE_2, pygame.K_2)
##                android.map_key(android.KEYCODE_3, pygame.K_3)
##                android.map_key(android.KEYCODE_4, pygame.K_4)
##                android.map_key(android.KEYCODE_5, pygame.K_5)
##                android.map_key(android.KEYCODE_6, pygame.K_6)
##                android.map_key(android.KEYCODE_7, pygame.K_7)
##                android.map_key(android.KEYCODE_8, pygame.K_8)
##                android.map_key(android.KEYCODE_9, pygame.K_9)
##              #  android.map_key(android.ACTION_DOWN, pygame.KEYDOWN)
##
##                for event in pygame.event.get():
##                    
##                    if event.type == pygame.KEYDOWN:
##                        username = ""
##                        if event.key == pygame.K_t:
##                            username += "t"
##                
##                #username = raw_input("Enter name: ")
                android.hide_keyboard()
            # Add the new highscore if it is high enough
            newscore = (username, score)
            highscore.append(newscore)
          
            highscore = sorted(highscore, key=itemgetter(1), reverse = True)
           
            del highscore[-1]
           

            # Clear file's contents
            f.close()
            f = open(filename, "w+")

            # Write the new high score table
            cPickle.dump(highscore, f)
            f.close()
            levelNum = 0
            score = 0
            username = "Anonymous"
          
            
        # Flip the display
        pygame.display.flip()
if __name__ == "__main__":
    main()
