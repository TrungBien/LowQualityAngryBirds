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


WIDTH = 1920
HEIGHT = 1080
RADIUS = 25

# circle_3 = Player()
# circle_3 = circle_3.circle(display, [pj.x, pj.y])

def create_border(width, height, center):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = center

    size = (width, height)
    rectangle = pymunk.Poly.create_box(body, size)
    rectangle.color = (0, 255, 0, 0) #RGBA
    rectangle.elasticity = 0.2
    rectangle.friction = 0.32
    return rectangle



def spawn_bird(mass, radius, position):
    body = pymunk.Body()
    body.position = position

    bird = pymunk.Circle(body, radius)
    bird.mass = mass
    bird.color = (255, 0, 0, 200) #RGBA
    bird.elasticity = 0.95
    bird.friction = 0.1
    
    return bird

    
def distance(mouse_pos, bird_pos):
    dx = mouse_pos[0] - bird_pos[0]
    dy = mouse_pos[1] - bird_pos[1]

    d = np.sqrt(dx**2 + dy**2)
    return d

def angle(mouse_pos, bird_pos):
    return math.atan2((mouse_pos[1] - bird_pos[1]), (mouse_pos[0] - bird_pos[0])) #we want radians

def Simulation(WIDTH, HEIGHT, RADIUS):
    time = 0
    
    display = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Low quality Angry Birds")
    circle_3 = Projectile_Motion(RADIUS)
    running = True
    background_color = "white"
    clock = pygame.time.Clock()
    

    simulation = pymunk.Space()
    simulation.gravity = (0, 981)

    options = pymunk.pygame_util.DrawOptions(display)
    mass = 5


    #bird
    bird = spawn_bird(mass, RADIUS, (100,100))
    simulation.add(bird.body, bird)

    #floor
    floor = create_border(WIDTH*5, RADIUS*2, (WIDTH/2, HEIGHT-RADIUS))
    simulation.add(floor.body, floor)
    
    while running:
        mouse = mouse_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Keyboard Events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    print("Reset")

            #Mouse Events                                    ### 1 - Left Click 
            if event.type == pygame.MOUSEBUTTONDOWN:         ### 2 - Middle Mouse Click
                if event.button == 1:                        ### 3 - Right CLick
                    
                    if bird:
                        line_distance = distance(mouse, bird.body.position)
                        proj_angle = angle(mouse, bird.body.position)
                        force_x = line_distance * math.cos(proj_angle) * 5
                        force_y = line_distance * math.sin(proj_angle) * 5
                        bird.body.apply_impulse_at_local_point((force_x, force_y), (0, 0))
                                                             ### 4 - Scroll Up
                                                             ### 5 - Scroll Down
            
            if bird:
                if bird.body.position[1] > 2000:
                    simulation.remove(bird)
                    print()
                else:
                    print(bird.body.position)
                    aim_line = [mouse, bird.body.position] 
                    pygame.draw.line(display, (0,0,0), aim_line[0], aim_line[1])



                       

                                                            

        display.fill(background_color)

       
        simulation.debug_draw(options)
        simulation.step(1/60)
        
        

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
        
        #circle_3.update(display)  ### Old

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
        
        
Simulation(WIDTH, HEIGHT, RADIUS)