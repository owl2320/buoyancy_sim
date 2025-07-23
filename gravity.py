import random

from pygame.locals import *
import pygame
import sys

#constants
g=0.5
speed_cap = -3

class Pseudo_Fluid:
    def __init__(self,x,y,size=(800,200),mass=5000,color='lightblue',k=1.2):
        self.x=x
        self.y=y
        self.g=g #g
        self.k=k #friction coefficient
        self.mass = mass
        self.size = size
        self.volume = self.size[0]*self.size[1] #considering breadth is 1m
        self.p = self.mass/self.volume #density

        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])

    def apply_effects(self,objects):
        for obj in objects:
            if self.rect.colliderect(obj.rect):
                obj.in_liquid = True #checks if it is submerged or not
                submerged_height = max(0,obj.rect.bottom-self.rect.top)
                submerged_volume = min(1,submerged_height/obj.size[1])
                F_B = self.p*self.g*obj.volume*submerged_volume #buoyancy force
                F_d = -0.5*self.k*obj.y_vel*abs(obj.y_vel) #drag force
                F_net = obj.weight-F_B+F_d #total force acting on the ball
                a = F_net/obj.mass #acceleration
                # #ensuring it doiesnt bounce unnecessarily
                # if self.rect.top - obj.size[1] * 2>obj.y + obj.y_vel + a:
                #     #other important values
                #     # pct_submersion = (obj.p/self.p) #how much it should be submerged
                #     # required_height = obj.size[1]*pct_submersion
                #
                #     # print('ALERT:IS IN BOUNCEING')
                #     # print('Covered VOLUME:',obj.rect.bottom-self.rect.top)
                #     # print()
                #     # print(self.rect.top-required_height)
                #     # obj.y += 10
                #     # a=0
                #     # print('A',a)
                #     # sys.exit()
                obj.y_vel+=a
                # print('obj', obj.weight, 'F_net', F_net) #stats
                # print('NEW_Y:',obj.y + obj.y_vel + a,self.rect.top)
                # print(self.rect.top - obj.size[1] * 2)
                # sys.exit()
            else:
                obj.in_liquid = False

    def draw(self):
        pygame.draw.rect(WIN,self.color,self.rect)

    def update(self):
        self.draw()
        self.apply_effects(balls)

class Object:
    def __init__(self,x,y,g=g,e=0.8,mass=2,size=(20,20),color='red',shape='circle'):
        self.x = x #positon
        self.y = y
        self.y_vel=0 #velocty
        self.g=g #gravitaional acceleration
        self.e=e #elasticity coefficient
        self.mass=mass #mass
        self.size = size #size
        self.volume = self.size[0]*self.size[1] #considering breadth is 1m
        self.p = self.mass/self.volume #density
        self.weight = self.mass*self.g #wight
        self.in_liquid = False #checks if it is in liquid
        self.show_text = False

        #other attributes
        self.color = color
        self.shape = shape
        self.font = pygame.font.Font(None, 32)

        self.rect = pygame.Rect(self.x,self.y,self.size[0],self.size[1])

    def apply_motion(self):
        if not self.in_liquid:
            self.y_vel += self.g
            # if self.y_vel>self.speed_cap: self.y_vel=self.speed_cap
        else:
            if self.y_vel<speed_cap:
                self.y_vel=speed_cap
        self.y += self.y_vel

        #ensire it doesnt go off the floor
        if self.y >= DIMENSIONS[1] - self.size[1]:
            self.y = DIMENSIONS[1] - self.size[1]
            if not self.in_liquid:self.y_vel *= -self.e
            else:self.y_vel=0

        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
        # print("V_Y:",self.y_vel,'Mass:',self.mass)
        # print('IN LIQUID:',self.in_liquid)

    def draw(self):
        if self.shape == 'circle':
            pygame.draw.ellipse(WIN, self.color, self.rect)
        elif self.shape == 'rectangle':
            pygame.draw.rect(WIN, self.color, self.rect)

        text = f'Mass:{self.mass},P:{self.p}'
        text_surface = self.font.render(str(text), True, (255, 255, 255))
        if self.show_text:
            WIN.blit(text_surface, (self.rect.x, self.rect.y - 20))

    def update(self):
        self.draw()
        self.apply_motion()
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.show_text = True
        else:
            self.show_text = False

pygame.init()
clock = pygame.time.Clock()

fps = 50
BG = 'lightgrey'
DIMENSIONS = (800, 600)
WIN = pygame.display.set_mode(DIMENSIONS)
pygame.display.set_caption('Gravity')

balls = [Object(100,10)]
pseudo_water = Pseudo_Fluid(0,400)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type==MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[2]:
                mass = random.randint(1,20)
                balls.append(Object(pygame.mouse.get_pos()[0],pygame.mouse.get_pos()[1],mass=mass))

    WIN.fill(BG)  # backround
    pseudo_water.update()
    for ball in balls:
        ball.update()

    pygame.display.update()
    clock.tick(fps)
