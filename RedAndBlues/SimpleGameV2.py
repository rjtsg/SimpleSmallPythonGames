import pygame
import random
import numpy as np
import matplotlib.pyplot as plt
pygame.init()


"""
What I want to create here is the following game:
x I want a green background
x I want Red Circles
x I want Blue triangles
x They will both move around randomly (~they should also not move out of the screen)
x If a blue triangle hits an other blue triangle they create a new blue triangle
x If a red circles hits another red circle they create a new red circle
x If a blue triangle hits a red circle they both dissapear
"""
"""
Next:
x add a day counter 1 day is 1s, thus the fps/count the number of times it goes through the while loop/fps
- Think of needs:
    sex
    food
    water
    sleep
- Think on how they move:
    satisfy needs
    hunt to win the game
    run away to stay alive

- Think about mutations (can be negative or positive):
    x velocity
    x collision_size
    x baby_time_plus
    - move_when

- Think of how they mate
    strongest survive so only they mate...
    female/male or it doesn't matter
    x they get the highest value + mutation
    they average + mutation
    some from 1, some from 2 + mutation <-- make this one
    x They should both be in their collision_size

- Blops do not live for ever
    x After x number of days let a blop die
    not have kids anymore?
    declining collision size?

- Visualize gene trends:
    - subplot
    - separate blue and red averages

"""

window_width = 500
window_height = 500
clock = pygame.time.Clock()
fps = 30
run = True
num_spec = 15
max_blops = 300
min_baby_time = 40
mutation_factor = 0.9
blops_life_number = 10 #how many days a blops continues to live

#Counters and data
day_counter = 0
DAYS = 0
red_species = []
blue_species = []
average_vel = []
average_collision_size = []
average_baby_time_plus = []

win = pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption('Reds&Blues')

#We will make one group: Blops

Blops = pygame.sprite.Group()

def MOVE(x,y,vel,move_counter,move_when, direction):
    if move_counter == move_when:
            direction = random.randint(0,4)
            move_counter = 0
    else:
            move_counter += 1

    if direction == 0: #do nothing
        pass
    if direction == 1: #move right
        x += vel
        if x > window_width:
            x -= vel
            # x -= window_width
    if direction == 2: #move left
        x -= vel
        if x < 0:
            x += vel
            # x += window_width
    if direction == 3: #move up
        y -= vel
        if y < 0:
            y += vel
            # y += window_height
    if direction == 4: #move down
        y += vel
        if y > window_height:
            y -= vel
            # y -= window_height
            
    return x,y, move_counter, direction

def Age(Blop):
    if Blop.age == blops_life_number*fps:
        Blop.kill()
    else:
        Blop.age += 1


def CollisionDetect():
    for Blop1 in Blops:
        for Blop2 in Blops:
            if Blop1 != Blop2: 
                distance_x = Blop1.x - Blop2.x
                distance_y = Blop1.y - Blop2.y
                distance = (distance_x**2 + distance_y**2)**0.5
                if distance < Blop1.collision_size:
                    both_in_range = False
                    if distance < Blop2.collision_size:
                        both_in_range = True
                    HandleCollision(Blop1,Blop2,both_in_range)
                    
def HandleCollision(Blop1,Blop2,both_in_range):
    if Blop1.team == Blop2.team and Blop1.baby_time >= min_baby_time and Blop2.baby_time >= min_baby_time and \
        len(Blops) < max_blops and both_in_range: 
        #to make sure the program doesn't get to big...
        min_dist = int(-Blop1.collision_size/2) #also make dependend on species size
        max_dist = int(Blop1.collision_size/2) # " "
        Blop1.baby_time = 0
        Blop2.baby_time = 0
        vel, collision_size, baby_time_plus = MutationBest(Blop1,Blop2)
        if Blop1.team == 'RED':
            baby_x = random.randint(min_dist,max_dist)
            baby_y = random.randint(min_dist,max_dist)
            x_ = Blop1.x
            y_ = Blop1.y
            new_x = baby_x + x_
            new_y = baby_x + y_
            Blops.add(RedCircle(new_x,new_y,vel,collision_size, baby_time_plus))
            # print('Red Baby')
        elif Blop1.team == 'BLUE':
            baby_x = random.randint(min_dist,max_dist)
            baby_y = random.randint(min_dist,max_dist)
            x_ = Blop1.x
            y_ = Blop1.y
            new_x = baby_x + x_
            new_y = baby_x + y_
            Blops.add(BlueTriangle(new_x,new_y,vel,collision_size, baby_time_plus))
            # print('Blue Baby')
        else:
            print('something is wrong')
    elif Blop1.team != Blop2.team:
        if both_in_range:
            Blop1.kill()
            Blop2.kill()
        else:
            Blop2.kill()

        # print('Kill')
    
def MutationBest(Blop1,Blop2):
    vel = max([Blop1.vel, Blop2.vel])
    collision_size = max([Blop1.collision_size, Blop2.collision_size])
    baby_time_plus = max([Blop1.baby_time_plus, Blop2.baby_time_plus])
    if random.random() > mutation_factor:
        vel += random.randint(-1,1)
        collision_size += random.randint(-5,5)
        baby_time_plus += random.randint(-1,1)

    return vel, collision_size, baby_time_plus    

class RedCircle(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, vel=None, collision_size=None,baby_time_plus=None):
        pygame.sprite.Sprite.__init__(self)
        if x == None and y == None and vel == None and collision_size == None and baby_time_plus == None:
            x = random.randint(10,490)
            y = random.randint(10,490)
            vel = 5
            collision_size = 30
            baby_time_plus = 1
        self.x = x
        self.y = y
        self.radius = 5
        self.colour = (255,0,0)
        self.vel = vel
        self.move_when = 5
        self.move_counter = self.move_when
        self.direction = 0
        self.team = 'RED'
        self.baby_time = 0
        self.baby_time_plus = baby_time_plus
        self.collision_size = collision_size
        self.age = 0
        
        
    def draw(self,win):
        self.RedCirlce_draw = pygame.draw.circle(win, self.colour, (self.x,self.y), self.radius)
        

    def move(self):
        self.x, self.y, self.move_counter, self.direction = MOVE(self.x,self.y, self.vel, self.move_counter, self.move_when, self.direction)
        self.baby_time += self.baby_time_plus
        
class BlueTriangle(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None, vel=None, collision_size=None, baby_time_plus=None):
        pygame.sprite.Sprite.__init__(self)
        if x == None and y == None and vel==None and collision_size == None and baby_time_plus == None:
            x = random.randint(10,490)
            y = random.randint(10,490)
            vel = 5
            collision_size = 30
            baby_time_plus = 1

        self.x = x
        self.y = y
        self.line_size = 10
        self.colour = (0,0,255)
        self.vel = vel
        self.move_when = 5
        self.move_counter = self.move_when
        self.direction = 0
        self.rect = win.get_rect()
        self.team = 'BLUE'
        self.baby_time = 0
        self.baby_time_plus = baby_time_plus
        self.collision_size = collision_size
        self.age = 0
        

    def draw(self,win):
        self.points = [(self.x,self.y), (self.x+self.line_size/2,self.y-self.line_size), (self.x+self.line_size,self.y)]
        pygame.draw.polygon(win, self.colour, self.points)

    def move(self):
        self.x, self.y, self.move_counter, self.direction = MOVE(self.x, self.y, self.vel, self.move_counter, self.move_when, self.direction)
        self.baby_time += self.baby_time_plus

for i in range(num_spec):
    Blops.add(RedCircle())
    Blops.add(BlueTriangle())
    


while run:
    day_counter += 1
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    win.fill((0,255,0))

    red_count = 0
    blue_count = 0
    all_vels = []
    all_collision_sizes = []
    all_baby_time_plusses = []

    for Blop in Blops:
        Blop.move()
        Blop.draw(win)
        Age(Blop)
        if Blop.team == 'RED':
            red_count += 1
        if Blop.team == 'BLUE':
            blue_count += 1
        all_vels.append(Blop.vel)
        all_collision_sizes.append(Blop.collision_size)
        all_baby_time_plusses.append(Blop.baby_time_plus)

    if red_count == 1 or blue_count == 1: #or len(Blops) == max_blops:
        run = False

    if day_counter % fps == 0:
        DAYS += 1
        red_species.append(red_count)
        blue_species.append(blue_count)
        average_vel.append(np.mean(all_vels))
        average_collision_size.append(np.mean(all_collision_sizes))
        average_baby_time_plus.append(np.mean(all_baby_time_plusses))

    CollisionDetect()   
    
    pygame.display.update()

print('The Simulation ran {} simulation days'.format(DAYS))    
pygame.quit()


plt.plot(red_species,'r')
plt.plot(blue_species,'b')
plt.legend(['red species', 'blue species'])
plt.title('Number of species per day')
plt.xlabel('Number of days')
plt.ylabel('Number of species')
plt.show()

plt.plot(average_vel)
plt.title('Average velocity of all blops')
plt.xlabel('Number of days')
plt.ylabel('Average velocity')
plt.show()

plt.plot(average_collision_size)
plt.title('Average collision_size')
plt.xlabel('Number of days')
plt.ylabel('Collision size')
plt.show()

plt.plot(average_baby_time_plus)
plt.title('Average time to get a new baby')
plt.xlabel('Number of days')
plt.ylabel('next baby time step')
plt.show()
