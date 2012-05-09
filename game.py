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
    
class Background (pygame.sprite.Sprite):
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

class Balloon (pygame.sprite.Sprite):
    
    def __init__(self, screen, init_x, init_y, dx, dy, image_file):
        '''constructor for balloon class, initialize the balloon'''
        pygame.sprite.Sprite.__init__(self)
        
        self.screen = screen
        
        self.x = init_x
        self.y = init_y
        self.dx = dx
        self.dy = dy
        
        self.image = pygame.transform.scale (load_image(image_file), (100, 200))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.image_w, self.image_h = self.image.get_size()
        
        self.active = True
        
    def update(self):
        '''update the balloon and check to make sure it hasn't moved off the screen'''
        if ((self.x + self.dx) <= 0):
            self.dx = self.dx * -1
        if ((self.x + self.dx) >= self.screen.get_size()[0]):
            self.dx = self.dx * -1
        if ((self.y + self.dy) <= 0):
            self.dy = self.dy * -1
        if ((self.y + self.dy) >= self.screen.get_size()[1]):
            self.dy = self.dy * -1
        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.topleft = (self.x, self.y)
    
    def draw(self):
        '''draw the balloon in its current position'''
        if self.active:
            self.screen.blit(self.image, self.rect)
            
            
class Enemy(pygame.sprite.Sprite):
    def __init__(self, screen, init_x, init_y, dx, dy, image_file, height, width):
        '''initialize the enemy sprite'''
        pygame.sprite.Sprite.__init__(self)
        
        self.screen = screen
        self.x = init_x
        self.y = init_y
        if self.x >= SCREEN_WIDTH / 2:
            dx = dx * -1
        self.dx = dx
        self.dy = dy
        
        self.image = pygame.transform.scale(load_image(image_file), (height, width))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.image_w, self.image_h = self.image.get_size()
        
        self.active = True
        
    def update(self):
        '''move and update the sprite'''
        if (self.rect.left < 0 - 3*self.image_w) or (self.rect.right > SCREEN_WIDTH + 3*self.image_w) or (self.rect.top < 0 - 3*self.image_h) or (self.rect.bottom > SCREEN_HEIGHT + 3* self.image_h):
           self.kill()
           self.active = False
        self.x += self.dx
        self.y += self.dy
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
    
    balloon_speed = 3
    moveRate = 2
    
    score = 0
    
    sky = Background(screen, scroll_speed, sky_image)

    # Map the back button to the escape key.
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        android.accelerometer_enable(True)

    # Use a timer to control FPS.
    pygame.time.set_timer(TIMEREVENT, 3000)
    pygame.time.set_timer(USEREVENT + 1, 1000)
    pygame.time.set_timer(USEREVENT + 2, 2000)
    pygame.time.set_timer(USEREVENT + 3, 4000)
    pygame.time.set_timer(USEREVENT + 4, 2000)
    
    pygame.key.set_repeat(FPS, FPS) # set key repeat on 
    
    balloon = Balloon(screen, SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT, 0, balloon_speed, "assets/balloon.gif")
    
    airplanes = pygame.sprite.Group()
    birds = pygame.sprite.Group()
    missiles = pygame.sprite.Group()
    
    spawn_pt = range(-200, -100) + range(SCREEN_WIDTH, SCREEN_WIDTH + 100)
    
    elapsed_time = 0
    
    while True:
        #game loop
        time_passed = clock.tick(FPS)
        elapsed_time += 1
        
        text = font.render("Score: " + str(score), 1, (0, 0, 0)) #render score
        
        if android:
            balloon_move = android.accelerometer_reading()
            if balloon.x >= 0 and balloon.x <= SCREEN_WIDTH - balloon.image_w:
                balloon.x = balloon.x - (balloon_move[0] * moveRate)
            elif balloon.x <= 0:   
                balloon.x += 1
            else:
                balloon.x -= 1
                    

            if android.check_pause():
                android.wait_for_resume()
                
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
                elif event.key == pygame.K_RIGHT:
                    if balloon.x <= SCREEN_WIDTH - balloon.image_w:
                        balloon.x += 5.0
                elif event.key == pygame.K_LEFT:
                    if balloon.x >= 0:
                        balloon.x -= 5.0
            elif event.type == USEREVENT + 1:
                score += 1
            elif event.type == TIMEREVENT and score>=2 and score<=10:
                airplanes.add(Enemy(screen, init_x, randint(-50, 200), randint(1, 5), randint(1, 3), enemy_image, 100, 50))
            
            elif event.type == USEREVENT + 2 and score>=10: 
                airplanes.add(Enemy(screen, init_x, randint(-50, 200), randint(1, 5), randint(1, 5), enemy_image, 100, 50))
                
            elif event.type == USEREVENT + 3:
                birds.add(Enemy(screen, init_x, randint(-50, SCREEN_HEIGHT + 50), randint(2,4), 0, "assets/balloon.gif", 80, 80))
                
            elif event.type == USEREVENT + 4:
                missiles.add(Enemy(screen, randint(0, SCREEN_WIDTH), SCREEN_HEIGHT, 0, randint(-8, -3), "assets/balloon.gif", 50, 120))
                print "missile"
                
        
        sky.update()
        sky.draw()
        
        balloon.update()
        balloon.draw()
        if balloon.y <= SCREEN_HEIGHT / 3:
            balloon.dy = 0
            sky.scrolling = True
        
        for enemy in airplanes:
            if pygame.sprite.collide_mask(enemy, balloon):
                # ADD GAME OVER SCREEN HERE
                if android:
                    android.vibrate(1)
                #return score
            enemy.update()
            enemy.draw()
            
        for bird in birds:
            bird.dy = 6*cos(0.1*elapsed_time) + 1
            if pygame.sprite.collide_mask(bird, balloon):
                # ADD GAME OVER SCREEN HERE
                if android:
                    android.vibrate(1)
                #return score
            bird.update()
            bird.draw()
            
        for missile in missiles:
            if pygame.sprite.collide_mask(missile, balloon):
                # ADD GAME OVER SCREEN HERE
                if android:
                    android.vibrate(1)
                #return score
            missile.update()
            missile.draw()
            
        screen.blit(text, (0,  SCREEN_HEIGHT - 30))
        pygame.display.flip()


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 0)
    game(screen)
