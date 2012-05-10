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
    
    def __init__(self, screen, init_x, init_y, dx, dy, image_file, lives):
        '''constructor for balloon class, initialize the balloon'''
        pygame.sprite.Sprite.__init__(self)
        
        self.screen = screen
        
        self.x = init_x
        self.y = init_y
        self.dx = dx
        self.dy = dy
        
        self.image = pygame.transform.scale (load_image(image_file), (132, 200))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.x, self.y)
        self.image_w, self.image_h = self.image.get_size()
        
        self.lives = lives
        
    def update(self, lives, img1, img2, img3, justcollided):
        '''update the balloon and check to make sure it hasn't moved off the screen'''
        self.lives = lives
        if  justcollided <= 0: 
            if lives > 7:
                self.image = img1
            if lives <= 7 and  lives >3:
                self.image = img2
            if lives <= 3:
                self.image = img3
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
        self.screen.blit(self.image, self.rect)
            
            
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
    balloon0 = pygame.transform.scale (load_image('assets/balloon.png'), (132, 200))
    balloon1 = pygame.transform.scale (load_image('assets/balloon1.png'), (132, 200))
    balloon2 = pygame.transform.scale (load_image('assets/balloon2.png'), (132, 200))
    balloonflashing = pygame.transform.scale (load_image('assets/balloonflash.png'), (132, 200))
    
    font = pygame.font.Font("assets/freesansbold.ttf", 30)
    try:
        mixer.music.load("assets/Scores.ogg")
        mixer.music.play(-1)
    except pygame.error:
        print "Couldn't find file."
    
    balloon_speed = 6
    moveRate = 2
    
    score = 0
    
    sky = Background(screen, scroll_speed, sky_image)

    # Map the back button to the escape key.
    if android:
        android.init()
        android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
        android.accelerometer_enable(True)

    # Use a timer to control FPS.
    pygame.time.set_timer(TIMEREVENT, 1000)
    pygame.time.set_timer(USEREVENT + 1, 3000)
    pygame.time.set_timer(USEREVENT + 2, 2000)
    pygame.time.set_timer(USEREVENT + 3, 4000)
    pygame.time.set_timer(USEREVENT + 4, 5000)
    pygame.time.set_timer(USEREVENT + 5, 8000)
    
    pygame.key.set_repeat(FPS, FPS) # set key repeat on 
    
    lives = 10
    
    balloon = Balloon(screen, SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT, 0, balloon_speed, "assets/balloon.png", lives)
    
    airplanes = pygame.sprite.Group()
    birds = pygame.sprite.Group()
    missiles = pygame.sprite.Group()
    
    powerups = pygame.sprite.Group()
    spawn_pt = range(-200, -100) + range(SCREEN_WIDTH, SCREEN_WIDTH + 100)
    elapsed_time = 0
    timer = 0
    justcollided = 0
    imagechanged = False
    
    
    while True:
        #game loop
        time_passed = clock.tick(FPS)
        elapsed_time += 1
        
        text = font.render("Score: " + str(score), 1, (0, 0, 0)) 
        #render score
        
        lives_txt = font.render("Lives: " + str(lives), 1, (0, 0, 0)) 
        
        timer -= 1
        justcollided -= 1
        
        if android:
            balloon_move = android.accelerometer_reading()
            if balloon.x >= 0 and balloon.x <= SCREEN_WIDTH - balloon.image_w:
                balloon.x = balloon.x - (balloon_move[0] * moveRate)
            elif balloon.x <= 0:   
                balloon.x += 1
            else:
                balloon.x -= 1
            if balloon.rect.bottom <= SCREEN_HEIGHT and balloon.y >= (SCREEN_HEIGHT - balloon.image_h)/2:
                balloon.y = balloon.y + ((balloon_move[1] - 5) * moveRate)
            elif balloon.rect.bottom >= SCREEN_HEIGHT:
                balloon.y -= 1
            else:
                balloon.y += 1
            
                    

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
                        balloon.x += balloon_speed
                elif event.key == pygame.K_LEFT:
                    if balloon.x >= 0:
                        balloon.x -= balloon_speed
                elif event.key == pygame.K_DOWN:
                    if balloon.y <= SCREEN_HEIGHT - balloon.image_h:
                        balloon.y += balloon_speed
                elif event.key == pygame.K_UP:
                    if balloon.y >= 0:
                        balloon.y -= balloon_speed
            elif event.type == TIMEREVENT:
                score += 1
            elif event.type == USEREVENT + 1 and score>=2 and score<=20:
                airplanes.add(Enemy(screen, init_x, randint(-50, 200), randint(1, 5), 3, enemy_image, (100, 50), 1, 1))
            
            elif event.type == USEREVENT + 2 and score>=50: 
                airplanes.add(Enemy(screen, init_x, randint(-50, 200), randint(1, 5), randint(3, 5), enemy_image, (100, 50), 1, 1))
                
            elif event.type == USEREVENT + 3 and score>=5:
                birds.add(Enemy(screen, init_x, randint(-50, SCREEN_HEIGHT + 50), randint(2,4), 0, "assets/balloon.gif", (80, 80), 1, 1))
                if score >=20 and score<40:
                    missiles.add(Enemy(screen, randint(0, SCREEN_WIDTH), SCREEN_HEIGHT, 0, randint(-8, -3), "assets/missile.png", (40, 150), 1, 1))
            elif event.type == USEREVENT + 4 and score>=50:
                missiles.add(Enemy(screen, randint(0, SCREEN_WIDTH), SCREEN_HEIGHT, 0, randint(-8, -3), "assets/missile.png", (40, 150), 1, 1))
        
            elif event.type == USEREVENT + 5 and score>=30:
                powerups.add(Enemy(screen, randint(100, SCREEN_WIDTH-100), 0, 0, 3, "assets/balloon.gif", (80, 80), 1, 1))
 
        if timer <= 20 and timer >= 0:
            sky.dy = 6
        elif timer > 25:
            sky.dy = -6
        else:
            sky.dy = 3
        
        sky.update()
        sky.draw()
      
        
           
        balloon.update(lives, balloon0, balloon1, balloon2, justcollided)
        balloon.draw()
        if balloon.y <= SCREEN_HEIGHT / 3:
            balloon.dy = 0
            sky.scrolling = True
        if justcollided <= 0:
            balloon.update(lives, balloon0, balloon1, balloon2, justcollided)
            
            for enemy in airplanes:
                if pygame.sprite.collide_mask(enemy, balloon):
                    # ADD GAME OVER SCREEN HERE
                    if android:
                        android.vibrate(0.3)
                    if lives <= 0:
                        return score
                    enemy.dy = 20
                    timer = 40
                    if score >= 10:
                        score -= 10
                    justcollided = 20
                    lives -= 1
                
            for bird in birds:
                if bird.dy != 20:
                    bird.dy = 6*cos(0.1*elapsed_time) + 1
                if pygame.sprite.collide_mask(bird, balloon):
                    # ADD GAME OVER SCREEN HERE
                    if android:
                        android.vibrate(0.3)
                    if lives <= 0:
                        return score
                    bird.dy = 20
                    timer = 30
                    if score >= 5:
                        score -= 5
                    justcollided = 20
                    lives -= 1
                
            for missile in missiles:
                if pygame.sprite.collide_mask(missile, balloon):
                    # ADD GAME OVER SCREEN HERE
                    if android:
                        android.vibrate(0.1)
                    missile.dy = 20
                    if lives <= 0:
                        return score
                    timer = 40
                    if score >= 15:
                        score -= 15
                    justcollided = 20
                    lives -= 1
                    
            for powerup in powerups:
                if pygame.sprite.collide_mask(powerup, balloon):
                    timer = 25
                    powerup.kill()
                    score += 10
        else:
           balloon.image = balloonflashing
           imagechanged = True
        airplanes.update()
        airplanes.draw(screen)
        birds.update()
        birds.draw(screen)
        missiles.update()
        missiles.draw(screen)
        powerups.update()
        powerups.draw(screen)
            
        screen.blit(text, (0,  SCREEN_HEIGHT - 30))
        screen.blit(lives_txt, (0, 0))
        pygame.display.flip()


if __name__ == "__main__":
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 0)
    game(screen)
