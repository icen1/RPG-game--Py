#importing modules
import pygame
from pygame.locals import *
import sys
import random
import time
from tkinter import filedialog
from tkinter import *

#Start pygame
pygame.init()

#Declaring Variables that will be used throught the game
vec = pygame.math.Vector2
HEIGHT = 350
WIDTH = 700
ACC = 0.3
FRIC = -0.10
FPS = 60
FPS_CLOCK = pygame.time.Clock()
COUNT = 0

#Cooldown
hit_cooldown = pygame.USEREVENT + 1
#Display
displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")

 # Run animation for the RIGHT
run_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Sprite2_R.png"),
             pygame.image.load("Player_Sprite3_R.png"),pygame.image.load("Player_Sprite4_R.png"),
             pygame.image.load("Player_Sprite5_R.png"),pygame.image.load("Player_Sprite6_R.png"),
             pygame.image.load("Player_Sprite_R.png")]
 
  # Run animation for the LEFT
run_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Sprite2_L.png"),
             pygame.image.load("Player_Sprite3_L.png"),pygame.image.load("Player_Sprite4_L.png"),
             pygame.image.load("Player_Sprite5_L.png"),pygame.image.load("Player_Sprite6_L.png"),
             pygame.image.load("Player_Sprite_L.png")]
 
# Attack animation for the RIGHT
attack_ani_R = [pygame.image.load("Player_Sprite_R.png"), pygame.image.load("Player_Attack_R.png"),
                pygame.image.load("Player_Attack2_R.png"),pygame.image.load("Player_Attack2_R.png"),
                pygame.image.load("Player_Attack3_R.png"),pygame.image.load("Player_Attack3_R.png"),
                pygame.image.load("Player_Attack4_R.png"),pygame.image.load("Player_Attack4_R.png"),
                pygame.image.load("Player_Attack5_R.png"),pygame.image.load("Player_Attack5_R.png"),
                pygame.image.load("Player_Sprite_R.png")]
 
# Attack animation for the LEFT
attack_ani_L = [pygame.image.load("Player_Sprite_L.png"), pygame.image.load("Player_Attack_L.png"),
                pygame.image.load("Player_Attack2_L.png"),pygame.image.load("Player_Attack2_L.png"),
                pygame.image.load("Player_Attack3_L.png"),pygame.image.load("Player_Attack3_L.png"),
                pygame.image.load("Player_Attack4_L.png"),pygame.image.load("Player_Attack4_L.png"),
                pygame.image.load("Player_Attack5_L.png"),pygame.image.load("Player_Attack5_L.png"),
                pygame.image.load("Player_Sprite_L.png")]

#Classes
class Background(pygame.sprite.Sprite):
     def __init__(self):
         super().__init__()
         self.bgimage = pygame.image.load("Background.png")
         self.bgY = 0
         self.bgX = 0
     def render(self):
         displaysurface.blit(self.bgimage, (self.bgX, self.bgY))
   
class Ground(pygame.sprite.Sprite):
     def __init__(self):
         super().__init__()
         self.image = pygame.image.load("Ground.png")
         self.rect = self.image.get_rect( center = (350,350))
     def render(self):
         displaysurface.blit(self.image, (self.rect.x, self.rect.y))
 
class Player(pygame.sprite.Sprite):
  def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player_Sprite_R.png")
        self.rect = self.image.get_rect()         
        #position and direction
        self.vx = 0
        self.pos = vec((340,240))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.direction = "RIGHT"
        
        #Movement 
        self.jumping = False
        self.running = False
        self.move_frame = 0
        
        #Comabt
        self.attacking = False
        self.attack_frame = 0
        self.cooldown = False
  def move(self):
        #keep a constant acceleration of 0.5 in the downwards direction(gravity)
        self.acc = vec(0,0.5)
         
        #Will set running to False if the player has slowed down to a certain extent
        if abs(self.vel.x) > 0.3:
            self.running = True
        else: 
            self.running = False
        
        #Returns the current key presses
        pressed_keys = pygame.key.get_pressed()
         
        # Accelerates the player in the direction of the key pressed
        if pressed_keys[K_LEFT]:
            self.acc.x = -ACC
        if pressed_keys[K_RIGHT]:
            self.acc.x = ACC
          
        #Formulas to calculate velocity while accounting for friction
        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc  # Updates Position with new values
         
        #This causes character warping from one point of the screen to the other
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
          
        #Update rect with new pos 
        self.rect.midbottom = self.pos 
     
  def gravity_check(self):
        hits = pygame.sprite.spritecollide(player, ground_group, False)
        if self.vel.y > 0:
            if hits:
                lowest = hits[0]
                if self.pos.y < lowest.rect.bottom:
                    self.pos.y = lowest.rect.top + 1
                    self.vel.y = 0
                    self.jumping = False
     
  def update(self):
        #Return to base frame at end of movement sequence
        if self.move_frame > 6:
            self.move_frame = 0
            return
          
        #Move the character to the next frame if at end of movement sequence 
        if self.jumping == False and self.running == True:
            if self.vel.x > 0:
                self.image = run_ani_R[self.move_frame]
                self.direction = "RIGHT"
            else:
                self.image = run_ani_L[self.move_frame]
                self.direction = "LEFT"
            self.move_frame += 1
             
        #Returns to base frame if standing still and incorrect frame is showing
        if abs(self.vel.x) < 0.2 and self.move_frame != 0:
            self.move_frame = 0
            if self.direction == "RIGHT":
                self.image = run_ani_R[self.move_frame]
            elif self.direction == "LEFT":
                self.image = run_ani_L[self.move_frame]
  
  def correction(self):
      #Function is used to correct the character postition when we attack while facing left
     if self.attack_frame == 1:
         self.pos.x -= 20
     if self.attack_frame == 10:
         self.pos.x += 20     
  def attack(self):
        #if attack sequence has reached the end of it return to base frame
        if self.attack_frame > 10:
            self.attack_frame = 0
            self.attacking = False
        #Check direction for correct animation to display
        if self.direction == "RIGHT":
            self.image = attack_ani_R[self.attack_frame]
        elif self.direction == "LEFT":
            self.correction()
            self.image = attack_ani_L[self.attack_frame]
            
        #Update the current attack frame
        self.attack_frame += 1
     
  def jump(self):
        self.rect.x += 1
         
        #Check to see if player is in contact with ground
        hits = pygame.sprite.spritecollide(self, ground_group, False)
         
        self.rect.x -= 1
         
        #if touching the ground and not currently jumping, cause the player to jump
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -12
    
  def player_hit(self):
      if self.cooldown == False:
         self.cooldown = True #Enable the cooldown 
         pygame.time.set_timer(hit_cooldown, 1000) #Resets cooldown
         print("hit")
         pygame.display.update()

class Enemy(pygame.sprite.Sprite): 
     def __init__(self):
         super().__init__()
         self.image= pygame.image.load("Enemy.png")
         self.rect = self.image.get_rect()
         self.pos = vec(0,0)
         self.vel = vec(0,0)
         self.direction = random.randint(0,1) #0 for right, 1 is left
         self.vel.x = random.randint(2,6) /2  #Randomised velocity of the generated enemy
         #Sets the intial position of the enemy
         if self.direction == 0:
             self.pos.x = 0
             self.pos.y = 235
         if self.direction == 1:
             self.pos.x = 700
             self.pos.y = 235
     def move(self):
         #Causes the enemy to change directions upon reaching the end of the screen
         if self.pos.x >= (WIDTH-20):
             self.direction = 1
         elif self.pos.x <= 0:
             self.direction = 0
         #Updates postion with new values
         if self.direction == 0:
             self.pos.x += self.vel.x
         elif self.direction == 1:
             self.pos.x -= self.vel.x
         #updates rect
         self.rect.center = self.pos
     def render(self):
         #Display the enemy on screen
         displaysurface.blit(self.image, (self.pos.x, self.pos.y))
     def update(self):
         #Checks for collision with the Player
         hits = pygame.sprite.spritecollide(self, Playergroup, False)
         #Activates when the two expressions are true
         if hits and player.attacking == True:
             self.kill()
             #print("Enemy killed")
         #if collision has occured and player not attacking, call "hit" function
         elif hits and player.attacking == False:
             player.player_hit()
#Creating objects
background = Background()
ground = Ground()
player = Player()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
enemy = Enemy()
Playergroup =pygame.sprite.Group()
Playergroup.add(player)

#Game loop
while True:
     player.gravity_check()
     for event in pygame.event.get():
         if event.type == QUIT:
             pygame.quit()
             sys.exit()
         
         #The event that happens when we click the mouse(left click)
         if event.type == pygame.MOUSEBUTTONDOWN:
             pass
         
         #Event handling for a range of different key presses
         if event.type == pygame.KEYDOWN:
             if event.key == pygame.K_SPACE:
                 player.jump()
             if event.key == pygame.K_RETURN:
                 if player.attacking == False:
                     player.attack()
                     player.attacking = True
         #Resetting the hit cooldown
         if event.type == hit_cooldown:
             player.cooldown = False
             pygame.time.set_timer(hit_cooldown, 0)
     #Rendering stuff
     player.update()
     if player.attacking == True:
         player.attack()
     player.move()
     background.render()
     ground.render()
     displaysurface.blit(player.image , player.rect)
     enemy.update()
     enemy.move()
     enemy.render()
     
     #Updating display and FPS
     pygame.display.update()
     FPS_CLOCK.tick(FPS)