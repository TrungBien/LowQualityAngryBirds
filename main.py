import numpy as np
import pygame
import pymunk
import pymunk.pygame_util
import matplotlib.pyplot as plt
import math
from scipy.integrate import ode



class Projectile_Motion():
    def __init__(self, radius=25):
        self.g = 9.81
        self.x = 25.
        self.y = 600.
        self.vy = -87.
        self.vx = 120.
        self.dt = 0.33
        self.t = 0
        self.radius = radius
        
        self.mass = 1.
        self.fr = 0.14
        
        self.r = ode(self.f)
        self.r.set_integrator("dop853")
        self.r.set_initial_value([self.y, self.vy], self.t)

    def f(self, t, y):
        return [y[1], (self.g*self.mass + self.fr * self.vy)/self.mass]
    
    def update(self, screen):
        if (self.y >= 720.- self.radius):
            self.vy *=-1.
            self.r.set_initial_value([self.y, (-self.vy)], self.t)
           

        if self.r.successful():
            self.r.integrate(self.r.t + self.dt)
            self.t = self.r.t
            self.y = self.r.y[0]
            self.vy = -self.r.y[1]
        print("this is vy %0.2f" % self.vy)
        
        self.x += (self.vx * self.dt)
        self.vx += ((self.vx * (-self.fr)) / self.mass) * self.dt 
        self.t += self.dt
        
        # print("This is vx: %0.2f" % self.vx)
        
        pygame.draw.circle(screen, (155,100,0), [self.x, self.y], self.radius)



class Player():

    def circle(screen, pos, radius=25):
        pygame.draw.circle(screen, (155,100,0), pos, radius)

    def positions():
        positions = []

def mouse_pos():
    mouse = pygame.mouse.get_pos()
    print(mouse)
    return mouse

def draw_circ(screen, pos):
    pygame.draw.circle(screen, (155,100,0), pos, 50)

class Collision:
    b = 0

class Simulation:
    a =1

pygame.init()


WIDTH = 1280
HEIGHT = 720
RADIUS = 25

# circle_3 = Player()
# circle_3 = circle_3.circle(display, [pj.x, pj.y])

def Simulation(WIDTH, HEIGHT):
    time = 0
    
    display = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Low quality Angry Birds")
    circle_3 = Projectile_Motion(RADIUS)
    running = True
    background_color = "white"
    clock = pygame.time.Clock()
    # circle_2 = [50, HEIGHT/2]

    # simulation = pymunk.Space()

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display.fill(background_color)

        clock.tick(60)
        time+=1/60

        # if (circle_2[0] < 1280-50):
        #     circle_2 = move(circle_2, 1)
        # else:
        #     print("Collision")
        # mouse_location = list(mouse_pos())


        #basic border collision

        # if (circle_3.y >= 720-50):
        #     circle_3.y = 720-50
        #     circle_3.vy *= -1
        #     circle_3.update(display)
        #     print(circle_3.vy)
        # else:
        #     circle_3.update(display)
        #     print(circle_3.vy)
        
        circle_3.update(display)

        # if (mouse_location[0] > 1280-50):
        #     mouse_location[0] = 1230
        #     draw_circ(display, mouse_location)
        # elif (mouse_location[0] < 50):
        #     mouse_location[0] = 50
        #     draw_circ(display, mouse_location)   
        # elif (mouse_location[1] > 720-50):
        #     mouse_location[1] = 720-50
        #     draw_circ(display, mouse_location)
        # elif (mouse_location[1] < 50):
        #     mouse_location[1] = 50
        #     draw_circ(display, mouse_location)

        
        # else:
        #     draw_circ(display, mouse_location)


        # if (circle_2[0] == 1280):
        #     print("Reached the end")
        #     print(time)
        # elif circle_2[0] == 1280-50:
        #     print("Circle edge hits border")
        # draw_circ(display, circle_2)
        
        # draw_circ(display, mouse_pos())
        #update window
        pygame.display.flip()
        
        
Simulation(WIDTH, HEIGHT)