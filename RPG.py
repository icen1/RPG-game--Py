#importing modules
import pygame
from pygame.locals import *
import sys
import random
import time
from tkinter import filedialog
from tkinter import *
import logging

#Start pygame
pygame.init()

#logging config
logging.basicConfig(filename="log.txt", level=logging.DEBUG,filemode="w",format="%(asctime)s:%(levelname)s:%(message)s",datefmt="%d/%m/%Y %I:%M:%S %p")

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

#Health animations 
health_ani = [pygame.image.load("heart0.png"), pygame.image.load("heart.png"),
              pygame.image.load("heart2.png"), pygame.image.load("heart3.png"),
              pygame.image.load("heart4.png"), pygame.image.load("heart5.png")]
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
        
        #Health
        self.health = 5
        
        #Score
        self.score = 0
        
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
           self.cooldown = True #Enable the cooldown as the player got hit
           pygame.time.set_timer(hit_cooldown, 1000) #Rests cooldown in 1 second
           
           self.health = self.health - 1
           health.image = health_ani[self.health]
           
           if self.health <= 0:
             self.kill()
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
             player.score += 1
             print("Enemy killed")
         #if collision has occured and player not attacking, call "hit" function
         elif hits and player.attacking == False:
             player.player_hit()

class Castle(pygame.sprite.Sprite):
     def __init__(self):
         super().__init__()
         self.hide = False
         self.image = pygame.image.load("castle.png")
     def update(self):
         if self.hide == False:
             displaysurface.blit(self.image, (400,85))

class EventHandler():
     def __init__(self):
         self.enemy_count = 0
         self.battle = False
         self.enemy_generation =  pygame.USEREVENT + 1
         self.stage_enemies= []
         self.stage = 1
         for x in range(1,21):
             self.stage_enemies.append(int((x ** 2/2) + 1))
     def stage_handler(self):
         #code for the tkinter stage selection window
         self.root = Tk()
         self.root.geometry("200x170")
         
         button1 = Button(self.root, text = "Twilight Dungeon",width = 18, height = 2, command = self.world1)
         button2 = Button(self.root, text = "Skyward Dungeon", width = 18, height = 2, command = self.world2)
         button3 = Button(self.root, text = "Hell Dungeon", width = 18, height = 2, command = self.world3)         
         
         button1.place(x = 40, y = 15)
         button2.place(x = 40, y = 65)
         button3.place(x = 40, y = 115)
         
         self.root.mainloop()
     def world1(self):
         self.root.destroy()
         pygame.time.set_timer(self.enemy_generation, 2000)
         castle.hide = True
         self.battle = True
     def world2(self):
         self.battle = True
         #Empty for now
     def world3(self):
         self.battle = True
         #Empty for now
     
     def next_stage(self): #Code for then the next stage is clicked
         self.stage += 1
         self.enemy_count = 0
         print("Stage: " + str(self.stage))
         pygame.time.set_timer(self.enemy_generation, 1500 - (50 * self.stage))
    
class HealthBar(pygame.sprite.Sprite):
     def __init__(self):
         super().__init__()
         self.image = pygame.image.load("heart5.png")
     def render(self):
         displaysurface.blit(self.image, (10,10))


#Creating objects
background = Background()
ground = Ground()
player = Player()
ground_group = pygame.sprite.Group()
ground_group.add(ground)
Playergroup =pygame.sprite.Group()
Playergroup.add(player)
castle = Castle()
handler = EventHandler()
Enemies = pygame.sprite.Group()
health = HealthBar()
e1 = Enemy()
E1 = pygame.sprite.Group()
E1.add(e1)



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
             if event.key == pygame.K_e and 450 < player.rect.x < 550:
                 handler.stage_handler()
             
             if event.key == pygame.K_SPACE:
                 player.jump()
             if event.key == pygame.K_RETURN:
                 if player.attacking == False:
                     player.attack()
                     player.attacking = True
             if event.key == pygame.K_n:
                 if handler.battle == True and len(Enemies) == 0:
                     handler.next_stage()
         #Resetting the hit cooldown
         if event.type == hit_cooldown:
             player.cooldown = False
             pygame.time.set_timer(hit_cooldown, 0)
         
         #Enemy generation 
         if event.type == handler.enemy_generation:
             if handler.enemy_count < handler.stage_enemies[handler.stage - 1]:
                 enemy = Enemy()
                 Enemies.add(enemy)
                 handler.enemy_count += 1
     #Rendering stuff
     player.update()
     if player.attacking == True:
         player.attack()
     player.move()
     background.render()
     ground.render()
     castle.update()
     for entity in Enemies:
         entity.update()
         entity.move()
         entity.render()
     if player.health > 0:
         displaysurface.blit(player.image , player.rect)
     health.render()
     Font = pygame.font.SysFont("Verdana", 20)
     printscore = Font.render("Kills: " +str(player.score), True, (118,74,74))
     displaysurface.blit(printscore,(WIDTH-90, 10))   
     #Updating display and FPS
     pygame.display.update()
     FPS_CLOCK.tick(FPS)
     
     #Logging
     logging.debug('Debug Information')
     logging.info('info Information')
     logging.warning('warning Information')
     logging.error('error Information')
     logging.critical('critical Information')