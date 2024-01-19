
# Modification date: Sun Feb  6 14:43:12 2022

# Production date: Sun Sep  3 15:42:59 2023

from random import randint
from random import choice
from math import sqrt
import pygame

wwidth = 768
wheight = 768
win = pygame.display.set_mode((wwidth,wheight))
pygame.init()

def distance(p, s):
    ps = (p.x + p.w//2, p.y + p.h//2)
    ss = (s.x + s.w//2, s.y + s.h//2)
    return int(sqrt((ps[0] - ss[0])**2 + (ps[1] - ss[1])**2))

rabbits = []
foods = []



class Food:
    nf = 0
    def __init__(self, x = randint(0, wwidth - 16), y = randint(0, wheight - 16)):
        self.edible = True
        self.type = "food"
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.colour = (123, 87, 43)

    def draw(self, win):
        pygame.draw.rect(win, self.colour, pygame.Rect(self.x, self.y, self.w, self.h))
    @classmethod
    def add_food(cls):
        cls.nf += 1


class Rabbit:
    np = 0
    def __init__(self, x = randint(0, wwidth - 32), y = randint(0, wheight - 32), i = 2):
        self.num = i
        self.type = "rabbit"
        self.w = 32
        self.h = 32
        self.x = x
        self.y = y
        self.colours = [(200, 200, 200), (0, 0, 0)]
        self.colour = self.colours[0]
        self.directions = ["left", "right", "up", "down"]
        self.direction = choice(self.directions)
        self.moving = False
        self.target = ""
        self.need = ""
        self.hunger = 200
        self.canmate = bool(self.hunger > 200)
        self.lt = []
        self.velocity = 3
        Rabbit.add_rabbit()
    




    def go_to_target(self, food, rabbit):
        self.search(food, rabbit)
        if self.target != "":
            if distance(self, self.target) < 30:#(self.x < self.target.x or self.x + self.w > self.target.x) and (self.y < self.target.y + self.target.h or self.y + self.h < self.target.y):
                if self.target.type == "rabbit":
                    if self != self.target:
                        rabbits.append(Rabbit(self.target.x, self.target.y))
                        self.hunger -= 100
                        self.target.hunger -= 100
                        self.target = ""
                    else:
                        self.target = ""
                elif self.target.type == "food":
                    try:
                        foods.remove(self.target)
                        self.target.edible = False
                        self.hunger += 300
                        self.target = ""
                    except:
                        self.search(food, rabbit)
            else:
                if self.target.type == "food" and self.target.edible or self.target.type == "rabbit" and self.target.canmate:
                    if self.x + self.w//4 < self.target.x + self.target.w//2:
                        self.x += self.velocity
                    elif self.x + (self.w//4)*3 > self.target.x + self.target.w//2:
                        self.x -= self.velocity
                    if self.y + self.h//4 < self.target.y + self.target.h//2:
                        self.y += self.velocity
                    elif self.y + (self.h//4)*3 > self.target.y + self.target.h//2:
                        self.y -= self.velocity
                else:
                    self.search(food, rabbit)
            



    def search(self, food, rabbits):
        self.canmate = bool(self.hunger > 200)
        if self.hunger < 150:
            self.lt = []
            for object in food:
                if object.edible:
                    self.lt.append([object, distance(self, object)])
            if len(self.lt) > 0:
                si = 0
                for j in range(len(self.lt)):
                    if self.lt[si][1] > self.lt[j][1]:
                        temp = j
                        si = temp
                try:
                    self.target = food[si]
                except:
                    return self.search(food, rabbits)
            else:
                self.target = ""

        elif self.canmate and self.hunger > 200:
            self.rl = []
            for object in rabbits:
                if object.canmate and object != self:
                    self.rl.append([object, distance(self, object)])
            if len(self.rl) > 0:
                si = 0
                for j in range(len(self.rl)):
                    if self.rl[si][1] > self.rl[j][1]:
                        temp = j
                        si = temp
                self.target = self.rl[si][0]
            else:
                self.target = ""
        else:
            self.target = ""
        



    
    def move_randomly(self, counter):
        if counter < 300:
            self.moving = True
        else:
            counter = 0
            self.direction = choice(self.directions)
        if self.moving:
            if self.direction == "left":
                if self.x > 0:
                    self.x -= self.velocity
                else:
                    self.x = 0
                    self.directions.remove("left")
                    self.direction = choice(self.directions)
                    self.directions.append("left")
                    
            if self.direction == "right":
                if self.x + self.w < wwidth:
                    self.x += self.velocity
                else:
                    self.x = wwidth - self.w
                    self.directions.remove("right")
                    self.direction = choice(self.directions)
                    self.directions.append("right")
                    
            if self.direction == "up":
                if self.y < 0:
                    self.y -= self.velocity
                else:
                    self.y = 0
                    self.directions.remove("up")
                    self.direction = choice(self.directions)
                    self.directions.append("up")
                    
            if self.direction == "down":
                if self.y + self.h < wheight:
                    self.y += self.velocity
                else:
                    self.y = wheight - self.h
                    self.directions.remove("down")
                    self.direction = choice(self.directions)
                    self.directions.append("down")
        return counter
    
    def draw(self, win):
        #pygame.draw.rect(win, self.colour, pygame.Rect(self.x, self.y, self.w, self.h))
        if self.hunger > 254 and self.canmate:
            pygame.draw.rect(win, (255, 255, self.hunger%255), pygame.Rect(self.x, self.y, self.w, self.h))
            pygame.draw.rect(win, (255, 255, 0), pygame.Rect(self.x + self.w, self.y, 12, 12))
        else:
            try:
                #print(self.hunger)
                pygame.draw.rect(win, (abs(self.hunger), abs(self.hunger), abs(self.hunger)), pygame.Rect(self.x, self.y, self.w, self.h))
            except:
                pass
        if self.target != "":
            if self.target.type == "rabbit":
                pygame.draw.rect(win, (70, 150, 70), pygame.Rect(self.x - 12, self.y + 12, 12, 12))
        if self.target == "":
            pygame.draw.rect(win, (0, 0, 0), pygame.Rect(self.x, self.y, 12, 12))
        else:
            pygame.draw.rect(win, (20, 70, 200), pygame.Rect(self.x + 12, self.y, 12, 12))
            pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.target.x -12, self.target.y - 12, 12, 12))
        if self.num == 0:
            pygame.draw.rect(win, (255, 0, 0), pygame.Rect(self.x -2, self.y - 2, 34, 34), 2)
        

    @classmethod
    def add_rabbit(cls):
        cls.np += 1



for i in range(2):
    dax = randint(0, wwidth - 32)
    day = randint(0, wheight - 32)
    rabbits.append(Rabbit(dax, day, i))

for i in range(30):
    dax = randint(0, wwidth - 16)
    day = randint(0, wheight - 16)
    foods.append(Food(dax, day))


"""
print(len(foods))
for i in range(len(foods)):
    print(foods[i].x)
print(len(rabbits))
"""
old_target = rabbits[0].target
old_direction = rabbits[0].direction
print("starting...")
clock = pygame.time.Clock()
running = True
dacounter = 0
thicc = 60
while running:
    clock.tick(thicc)
    win.fill((20, 200, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    

    counter = dacounter
    for rabbit in rabbits:
        if rabbit.hunger < 0:
            rabbits.remove(rabbit)
            del rabbit
            continue
        if rabbit.target == "":
            rabbit.search(foods, rabbits)
        if rabbit.target != "":
            rabbit.go_to_target(foods, rabbits)
        else:
            
            dacounter = rabbit.move_randomly(counter)
    

    if len(rabbits) > 0:
        if old_direction != rabbits[0].direction:
            #print(rabbits[0].direction)
            old_direction = rabbits[0].direction
        
        if old_target != rabbits[0].target:
            #print(rabbits[0].target)
            old_target = rabbits[0].target
    
    if rabbits[0].target != "":
        print(len(rabbits), rabbits[0].x, rabbits[0].y, rabbits[0].hunger, rabbits[0].target.type, rabbits[0].target.x, rabbits[0].target.y)
    else:
        print(len(rabbits), rabbits[0].x, rabbits[0].y, rabbits[0].hunger)
    
    pygame.draw.rect(win, (255, 0, 0), pygame.Rect(rabbits[0].x - 2, rabbits[0].y - 2, rabbits[0].w + 2, rabbits[0].h + 2))



    if dacounter % 10 == 0:
        dax = randint(0, wwidth - 16)
        day = randint(0, wheight - 16)
        foods.append(Food(dax, day))
    for rabbit in rabbits:
        if dacounter % 10 == 0:
            rabbit.hunger -= 1
            
    

    for i in range(len(foods)):
        foods[i].draw(win)
    for i in range(len(rabbits)):
        rabbits[i].draw(win)

    dacounter += 1
    pygame.display.update()