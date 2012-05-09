import pygame, sys, random, time, pickle
from pygame.locals import *
from random import *



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
                filename = "highscores.text"
            else:
                filename = "highscores.txt" 
            highscore = [0, 0, 0, 0, 0, 0, 0, 0]
            try: # If there is already a highscores file, try opening it
                f = open(filename, "r+")
            except IOError: # If there is no highscores file, create one and add 0's to it
                f = open(filename, "w+")
                pickle.dump(highscore, f)
                f.seek(0)
            try:
                    highscore = pickle.load(f)
            except EOFError:
                    pass # Just don't load anything

            # Add the new highscore if it is high enough
            highscore.append(score)
            highscore.sort()
            highscore.reverse()
            del highscore[-1]
           

            # Clear file's contents
            f.close()
            f = open(filename, "w+")

            # Write the new high score table
            pickle.dump(highscore, f)
            f.close()
            levelNum = 0
          
            
        # Flip the display
        pygame.display.flip()
if __name__ == "__main__":
    main()
