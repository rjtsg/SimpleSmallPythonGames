import pygame
import numpy as np
import math
pygame.init()

window_width = 600
window_height = 600
time_step = 1
fps = 30
clock = pygame.time.Clock()
run = True
gravitational_constant = 0.674

win = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Solar system')

def VelocityUpdate():
    for planet1 in Planets:
        for planet2 in Planets:
            if planet1 != planet2:
                sqr_dist = ((planet1.position[0] - planet2.position[0])**2 + (planet1.position[1] - planet2.position[1])**2)**0.5
                x_direction = planet2.position[0] - planet1.position[0]
                y_direction = planet2.position[1] - planet1.position[1]
                max_direction = max([abs(x_direction), abs(y_direction)])
                x_direction_norm = x_direction/max_direction
                y_direction_norm = y_direction/max_direction
                normalized_direction = np.array([x_direction_norm, y_direction_norm])
                force = normalized_direction * gravitational_constant * planet1.mass * planet2.mass / sqr_dist**2
                acceleration = force / planet1.mass
                velocity_x = planet1.velocity[0] + acceleration[0] * time_step
                velocity_y = planet1.velocity[1] + acceleration[1] * time_step
                planet1.velocity = np.array([velocity_x, velocity_y])
                
                

def PositionUpdate():
    for planet in Planets:
        x = planet.position[0] + planet.velocity[0] * time_step
        y = planet.position[1] + planet.velocity[1] * time_step
        planet.position = (x,y)
        if x - int(x) <= 0.5:
            x_int = math.floor(x)
        else:
            x_int = math.ceil(x)
        if y - int(y) <= 0.5:
            y_int = math.floor(y)
        else:
            y_int = math.ceil(y)
        planet.position_int = (x_int,y_int)
        

class Planet(pygame.sprite.Sprite):
    def __init__(self,position,color, radius, mass, velocity=np.array([0,0])):
        pygame.sprite.Sprite.__init__(self)
        self.position = position
        self.position_int = position
        self.radius = radius
        self.color = color
        self.mass = mass
        self.velocity = velocity
        
    
    def draw(self,win):
        self.planet_draw = pygame.draw.circle(win, self.color, self.position_int, self.radius)


Planets = pygame.sprite.Group()
Planets.add(Planet((300,300),(255,0,0),10,1000))
Planets.add(Planet((450,300),(0,0,255),10,10,np.array([0,-2.5])))
Planets.add(Planet((470,300),(255,255,255),2,0.0001,np.array([0, -3.03])))

while run:
    clock.tick(fps)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    win.fill((0,0,0))

    for Planet in Planets:
        Planet.draw(win)
        

    VelocityUpdate()
    PositionUpdate()
    
    pygame.display.update()

    

pygame.quit()


