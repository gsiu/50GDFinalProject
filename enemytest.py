import pygame, sys, random, time
from pygame.locals import *
from random import *
from math import *

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
FPS = 40

# Screen constants
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 500
SCREENRECT = Rect(0, 0, 480, 500)

def load_image(file_name):
    '''load images with exception handling'''
    try:
        image = pygame.image.load(file_name)
    except pygame.error, message:
        print "Cannot open image: " + file_name
        raise SystemExit, message
    return image.convert_alpha()
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, init_x, init_y, dx, dy, image_file, (height, width), numrows, numcols):
        '''initialize the enemy sprite'''
        pygame.sprite.Sprite.__init__(self)
        
        self.screen = screen
        self.x = init_x
        self.y = init_y
        if self.x >= SCREEN_WIDTH / 2:
            dx = dx * -1
        self.dx = dx
        self.dy = dy
        
        self.sheet = load_image(image_file)
        self.frame = []
        self.frame_index = 0        
        
        # Get the image's width and height
        self.image_w, self.image_h = self.sheet.get_size()[0] / numrows, self.sheet.get_size()[1] / numcols
        
        for i in range(numrows * numcols):
            self.frame.append(pygame.transform.scale(load_image(image_file), (height, width)))
            
        
        # Load each frame as a subsurface in animation
        for j in range(numcols):
            for i in range(numrows):
                self.frame.append(pygame.transform.scale(self.sheet.subsurface(Rect(i * self.image_w, j, self.image_w, self.image_h)), (height, width)))
        
        self.image = self.frame[self.frame_index]
        self.rect = self.frame[self.frame_index].get_rect()
        self.rect.topleft = (self.x, self.y)
        
        self.active = True
        
    def update(self):
        '''move and update the sprite'''
        if (self.rect.left < 0 - 3*self.image_w) or (self.rect.right > SCREEN_WIDTH + 3*self.image_w) or (self.rect.top < 0 - 3*self.image_h) or (self.rect.bottom > SCREEN_HEIGHT + 3* self.image_h):
           self.kill()
           self.active = False
        self.x += self.dx
        self.y += self.dy
        self.frame_index = (self.frame_index + 1) % len(self.frame)
        self.image = self.frame[self.frame_index]
        self.rect.topleft = (self.x, self.y)
    
    def draw(self):
        '''if the enemy is active, draw it to the screen'''
        if self.active:
            self.screen.blit(self.image, self.rect)
     
def game(screen):
    '''main function that runs the game'''
    pygame.init()
    window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Sky High')
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    scroll_speed = 3
    
    sky_image = "assets/sky.gif"
    font = pygame.font.Font("assets/freesansbold.ttf", 30)
    try:
        mixer.music.load("assets/Scores.ogg")
        #mixer.music.play(-1)
    except pygame.error:
        print "Couldn't find file."
    
    balloon_speed = 6
    moveRate = 2
    
    score = 0
    
    # Map the back button to the escape key.
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        android.accelerometer_enable(True)

    # Use a timer to control FPS.
    pygame.time.set_timer(TIMEREVENT, 1000)
    pygame.time.set_timer(USEREVENT + 1, 3000)
    pygame.time.set_timer(USEREVENT + 2, 5000)
    pygame.time.set_timer(USEREVENT + 3, 10000)
    pygame.time.set_timer(USEREVENT + 4, 3500)
    pygame.time.set_timer(USEREVENT + 5, 8000)
    
    pygame.key.set_repeat(FPS, FPS) # set key repeat on 
    
    birds = pygame.sprite.Group()
    
    spawn_pt = range(-200, -100) + range(SCREEN_WIDTH, SCREEN_WIDTH + 100)
    
    elapsed_time = 0
    
    timer = 0
    
    while True:
        screen.fill((0,0,0))
        #game loop
        time_passed = clock.tick(FPS)
        elapsed_time += 1
        
        text = font.render("Score: " + str(score), 1, (255, 0, 0)) #render score
        
        timer -= 1
        
                       
        #Randomly choose a spawn point from the list
        init_x = choice(spawn_pt)
        
        if init_x < SCREEN_WIDTH/2:
            enemy_image = "assets/plane-right.gif"
        else:
            enemy_image = "assets/plane-left.gif"
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == TIMEREVENT:
                score += 1
              
            elif event.type == USEREVENT + 3:
                birds.add(Enemy(screen, init_x, randint(-50, SCREEN_HEIGHT + 50), randint(2,4), 0, "assets/bird.png", (80, 80), 1, 1))
            
        for bird in birds:
            bird.dy = 6*cos(0.1*elapsed_time) + 1
        birds.update()
        birds.draw(screen)
            
        screen.blit(text, (0,  SCREEN_HEIGHT - 30))
        pygame.display.flip()


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 0)
    game(screen)
