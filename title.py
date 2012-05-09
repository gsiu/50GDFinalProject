import pygame, sys, random, time
from pygame.locals import *
from random import *

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

def load_image(file_name):
    '''load images with exception handling'''
    try:
        image = pygame.image.load(file_name)
    except pygame.error, message:
        print "Cannot open image: " + file_name
        raise SystemExit, message
    return image.convert_alpha()


class Backgrounds (pygame.sprite.Sprite):
    def __init__(self, screen, speed, image_file):
        pygame.sprite.Sprite.__init__(self)
        
        self.screen = screen
        self.scrolling = False
        
        self.image = load_image(image_file)
        self.rect = self.image.get_rect()
        self.image_w, self.image_h = self.image.get_size()
        
        self.dy = speed
        self.rect.bottom = SCREEN_HEIGHT
        
    def update(self):
        if self.scrolling == True:
            self.rect.bottom += self.dy
        if self.rect.top >= 0:
            self.rect.bottom = SCREEN_HEIGHT
            
    def draw(self):
        self.screen.blit(self.image, self.rect)

class Balloons (pygame.sprite.Sprite):
    
    def __init__(self, screen, init_x, init_y, dx, dy, image_file, image2_file):
        '''constructor for balloon class, initialize the balloon'''
        pygame.sprite.Sprite.__init__(self)
        
        self.screen = screen
        
        self.x = init_x
        self.y = init_y
        self.dx = dx
        self.dy = dy
        
        self.image = pygame.transform.scale (load_image(image_file), (200, 300))
        self.image2 = pygame.transform.scale (load_image(image2_file), (200, 300))
        self.rect = self.image.get_rect()
        self.rect.move(self.x, self.y)
        self.rect.topleft = (self.x, self.y)
        self.image_w, self.image_h = self.image.get_size()
        self.rect.bottomright = (self.x + self.image_w, self.y + self.image_h)
        
        self.active = False
        
    def update(self):
        '''update the balloon and check to make sure it hasn't moved off the screen'''
        pass
    def draw(self):
        '''draw the balloon in its current position'''
        if self.active:
            self.screen.blit(self.image2, (self.x, self.y))
        else:
            self.screen.blit(self.image, (self.x, self.y))
            
  
     
    
    
def title(screen):
    '''main function that runs the game'''
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Sky High')
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    scroll_speed = 3
    
    menu_image = "assets/menu.png"
    play_image = "assets/play.png"
    played_image = "assets/play_pressed.png"
    highscore_image = "assets/highscore.png"
    highscored_image = "assets/highscore_pressed.png"
    exit_image = "assets/exit.png"
    exited_image = "assets/exit_pressed.png"
    font = pygame.font.Font("assets/freesansbold.ttf", 30)
    try:
        mixer.music.load("assets/Scores.ogg")
        mixer.music.play(-1)
    except pygame.error:
        print "Couldn't find file."
    
    balloon_speed = 3
    moveRate = 2
    
    score = 0
    
    background = (0, 0, 0)
    
    sky = Backgrounds(screen, scroll_speed, menu_image)

    # Map the back button to the escape key.
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        android.accelerometer_enable(True)

    # Use a timer to control FPS.
    pygame.time.set_timer(TIMEREVENT, 3000)
    pygame.time.set_timer(USEREVENT + 1, 1000)
    pygame.time.set_timer(USEREVENT + 2, 2000)
    
    pygame.key.set_repeat(FPS, FPS) # set key repeat on 
    
    play = Balloons(screen, SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT/2 - 330, 0, balloon_speed, play_image, played_image)
    highscore = Balloons(screen, SCREEN_WIDTH / 2 - 230, SCREEN_HEIGHT/2 - 150, 0, balloon_speed, highscore_image, highscored_image)
    getout = Balloons(screen, SCREEN_WIDTH / 2 +30, SCREEN_HEIGHT/2 +10, 0, balloon_speed, exit_image, exited_image)
       
    while True:
        #game loop
        time_passed = clock.tick(FPS)
        
        if android:

            if android.check_pause():
                android.wait_for_resume()
                
        init_x = randint(0, SCREEN_WIDTH)
        
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if getout.rect.collidepoint(event.pos):
                        getout.active = True
                        screen.fill(background)
                        sky.draw()
                        play.draw()
                        highscore.draw()
                        getout.draw()
                        pygame.display.flip()
                    elif play.rect.collidepoint(event.pos):
                        play.active = True
                        screen.fill(background)
                        sky.draw()
                        play.draw()
                        highscore.draw()
                        getout.draw()
                        pygame.display.flip()
                    elif highscore.rect.collidepoint(event.pos):
                        highscore.active = True
                        screen.fill(background)
                        sky.draw()
                        play.draw()
                        highscore.draw()
                        getout.draw()
                        pygame.display.flip()
                
            elif event.type == pygame.MOUSEBUTTONUP:
                highscore.active = False
                play.active = False
                getout.active = False
                if event.button == 1:
                    if getout.rect.collidepoint(event.pos):
                        sys.exit(0)
                        pygame.quit()
                    elif play.rect.collidepoint(event.pos):
                        mixer.music.fadeout(500)
                        return 99
                    elif highscore.rect.collidepoint(event.pos):
                        mixer.music.fadeout(500)
                        return 100
                
                
        screen.fill(background)
        
        sky.update()
        sky.draw()
        
        play.update()
        play.draw()

        highscore.update()
        highscore.draw()

        getout.update()
        getout.draw()
        
        pygame.display.flip()

if __name__ == "__main__":
    main()
