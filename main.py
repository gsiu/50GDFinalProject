import pygame, sys, random, time
from pygame.locals import *
from random import *



from title import *
from game import *

try:
    import android
except ImportError:
    android = None

try: 
    import pygame.mixer as mixer    
except ImportError:
    import android.mixer as mixer
    
# Event constant.
TIMEREVENT = pygame.USEREVENT

# The FPS the game runs at.
FPS = 35

# Screen constants
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 800
SCREENRECT = Rect(0, 0, 480, 800)

if __name__ == "__main__":

    # Check if sound and font are supported
    if not pygame.font:
        print "Warning, fonts disabled"
   
    
    # Constants
    FPS = 35
    SCREEN_WIDTH, SCREEN_HEIGHT = 480, 800
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
            #levelNum = scores(screen)
            # Returns 0 when player exits highscore screen
            levelNum = 0

        else: # levelNum == 99:
            t = game(screen)
            score = score + int(t)
            levelNum = 0
          
            
        # Flip the display
        pygame.display.flip()
