import pygame
import random
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

- Think about mutations:
    velocity
    collision_size
    baby_time_plus
    move_when

- Think of how they mate
    strongest survive so only they mate...
    female/male or it doesn't matter
    they get the highest value + mutation
    they average + mutation
    some from 1, some from 2 + mutation

"""

window_width = 500
window_height = 500
clock = pygame.time.Clock()
fps = 30
run = True
num_spec = 10
max_blops = 100
min_baby_time = 50

#Counters and data
day_counter = 0
DAYS = 0
red_species = []
blue_species = []

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
            x -= window_width
    if direction == 2: #move left
        x -= vel
        if x < 0:
            x += window_width
    if direction == 3: #move up
        y -= vel
        if y < 0:
            y += window_height
    if direction == 4: #move down
        y += vel
        if y > window_height:
            y -= window_height
            
    return x,y, move_counter, direction


def CollisionDetect():
    for Blop1 in Blops:
        for Blop2 in Blops:
            if Blop1 != Blop2: 
                distance_x = Blop1.x - Blop2.x
                distance_y = Blop1.y - Blop2.y
                distance = (distance_x**2 + distance_y**2)**0.5
                if distance < Blop1.collision_size:
                    HandleCollision(Blop1,Blop2)
                    

                
def HandleCollision(Blop1,Blop2):
    if Blop1.team == Blop2.team and Blop1.baby_time >= min_baby_time and Blop2.baby_time >= min_baby_time and len(Blops) < max_blops: 
        #to make sure the program doesn't get to big...
        min_dist = int(-Blop1.collision_size/2) #also make dependend on species size
        max_dist = int(Blop1.collision_size/2) # ""
        Blop1.baby_time = 0
        Blop2.baby_time = 0
        if Blop1.team == 'RED':
            baby_x = random.randint(min_dist,max_dist)
            baby_y = random.randint(min_dist,max_dist)
            x_ = Blop1.x
            y_ = Blop1.y
            new_x = baby_x + x_
            new_y = baby_x + y_
            Blops.add(RedCircle(new_x,new_y))
            print('Red Baby')
        elif Blop1.team == 'BLUE':
            baby_x = random.randint(min_dist,max_dist)
            baby_y = random.randint(min_dist,max_dist)
            x_ = Blop1.x
            y_ = Blop1.y
            new_x = baby_x + x_
            new_y = baby_x + y_
            Blops.add(BlueTriangle(new_x,new_y))
            print('Blue Baby')
        else:
            print('something is wrong')
    elif Blop1.team != Blop2.team:
        Blop1.kill()
        Blop2.kill()
        print('Kill')
    
    

class RedCircle(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None):
        pygame.sprite.Sprite.__init__(self)
        if x == None and y == None:
            x = random.randint(10,490)
            y = random.randint(10,490)
        self.x = x
        self.y = y
        self.radius = 5
        self.colour = (255,0,0)
        self.vel = 5
        self.move_when = 5
        self.move_counter = self.move_when
        self.direction = 0
        self.team = 'RED'
        self.baby_time = 0
        self.baby_time_plus = 1
        self.collision_size = 30
        
        
    def draw(self,win):
        self.RedCirlce_draw = pygame.draw.circle(win, self.colour, (self.x,self.y), self.radius)
        

    def move(self):
        self.x, self.y, self.move_counter, self.direction = MOVE(self.x,self.y, self.vel, self.move_counter, self.move_when, self.direction)
        self.baby_time += self.baby_time_plus
        
class BlueTriangle(pygame.sprite.Sprite):
    def __init__(self, x=None, y=None):
        pygame.sprite.Sprite.__init__(self)
        if x == None and y == None:
            x = random.randint(10,490)
            y = random.randint(10,490)
        self.x = x
        self.y = y
        self.line_size = 10
        self.colour = (0,0,255)
        self.vel = 5
        self.move_when = 5
        self.move_counter = self.move_when
        self.direction = 0
        self.rect = win.get_rect()
        self.team = 'BLUE'
        self.baby_time = 0
        self.baby_time_plus = 1
        self.collision_size = 30
        

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

    for Blop in Blops:
        Blop.move()
        Blop.draw(win)
        if Blop.team == 'RED':
            red_count += 1
        if Blop.team == 'BLUE':
            blue_count += 1

    if red_count == 1 or blue_count == 1:
        run = False

    if day_counter % fps == 0:
        DAYS += 1
        red_species.append(red_count)
        blue_species.append(blue_count)

    CollisionDetect()   
    
    pygame.display.update()

print('The Simulation ran {} number of simulation days'.format(DAYS))    
pygame.quit()


plt.plot(red_species,'r')
plt.plot(blue_species,'b')
plt.legend(['red species', 'blue species'])
plt.title('Number of species per day')
plt.xlabel('Number of days')
plt.ylabel('Number of species')
plt.show()