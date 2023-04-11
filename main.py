import numpy as np
import pygame
import pymunk
import pymunk.pygame_util
import matplotlib.pyplot as plt
import math
from scipy.integrate import ode





pygame.init()


WIDTH = 1920
HEIGHT = 1080
RADIUS = 25



def mouse_pos():
    mouse = pygame.mouse.get_pos()
    #print(mouse)
    return mouse

def wood_structure(width, height, center):
    body = pymunk.Body(body_type=pymunk.Body.DYNAMIC)
    body.position = center

    size = (width, height)
    wood = pymunk.Poly.create_box(body, size, radius=1)
    wood.color = (92, 64, 51, 0)
    wood.elasticity = 0.5
    wood.friction = 0.4
    wood.mass = 20
    wood.collision_type = 3

    return wood



def create_border(width, height, center):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = center

    size = (width, height)
    rectangle = pymunk.Poly.create_box(body, size)
    rectangle.color = (0, 255, 0, 0) #RGBA
    rectangle.elasticity = 0.7
    rectangle.friction = 0.50
    rectangle.mass = 5.0
    return rectangle


def spawn_pig(mass, radius, position):
    body = pymunk.Body()
    body.position = position

    pig = pymunk.Circle(body, radius)
    pig.mass = mass
    pig.color = (0, 100, 0, 100)
    pig.elasticity = 0.5
    pig.friction = 0.5
    pig.collision_type = 2

    return pig

def spawn_bird(mass, radius, position):
    body = pymunk.Body()
    body.position = position

    bird = pymunk.Circle(body, radius)
    bird.mass = mass
    bird.color = (255, 0, 0, 200) #RGBA
    bird.elasticity = 0.95
    bird.friction = 0.14
    bird.collision_type = 1
    
    return bird

    
def distance(mouse_pos, bird_pos):
    dx = mouse_pos[0] - bird_pos[0]
    dy = mouse_pos[1] - bird_pos[1]

    d = np.sqrt(dx**2 + dy**2)
    return d

def angle(mouse_pos, bird_pos):
    return math.atan2((mouse_pos[1] - bird_pos[1]), (mouse_pos[0] - bird_pos[0])) #we want radians

def pig_hit(sim, arbiter, data):
    print("Pig is hit!")
    
    return True

def pig_crush(sim, arbiter, data):
    print("Pig is hurt by wood structure!")
    
    return True



def Simulation(WIDTH, HEIGHT, RADIUS):
    time = 0
    
    display = pygame.display.set_mode((WIDTH,HEIGHT))
    pygame.display.set_caption("Low quality Angry Birds")
    running = True
    background_color = "white"
    clock = pygame.time.Clock()
    

    simulation = pymunk.Space()
    simulation.gravity = (0, 981)

    options = pymunk.pygame_util.DrawOptions(display)
    mass = 4


    #bird
    bird = spawn_bird(mass, RADIUS, (100,1000))
    simulation.add(bird.body, bird)

   
    #floor
    floor = create_border(WIDTH, RADIUS*1.8, (WIDTH/2, HEIGHT-RADIUS))
    left_wall = create_border(RADIUS*2, HEIGHT*10, (RADIUS, HEIGHT/2))
    right_wall = create_border(RADIUS*2, HEIGHT*10, (WIDTH, HEIGHT/2))
    ceiling = create_border(WIDTH, RADIUS*1.8, (WIDTH/2, RADIUS))
    wood = wood_structure(60, 200, (1000, 600))
    

    
    simulation.add(floor.body, floor)
    simulation.add(left_wall.body, left_wall)
    simulation.add(right_wall.body, right_wall)
    simulation.add(ceiling.body, ceiling)
    simulation.add(wood.body, wood)

    bird_fly = False
    pig_num = 0
    pigs = []

    bird_pig = simulation.add_collision_handler(1,2)
    bird_pig.begin = pig_hit

    pig_wood = simulation.add_collision_handler(3,2)
    pig_wood.begin = pig_crush

    while running:
        mouse = mouse_pos()
        display.fill(background_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Keyboard Events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if event.key == pygame.K_r:
                    
                    print("Reset")
                    return Simulation(WIDTH, HEIGHT, RADIUS)
                if event.key == pygame.K_n:
                    wood_vertical = wood_structure(60, 200, mouse)
                    simulation.add(wood_vertical.body, wood_vertical)

                if event.key == pygame.K_m:
                    wood_horizontal = wood_structure(200, 60, mouse)
                    simulation.add(wood_horizontal.body, wood_horizontal)

            #Mouse Events                                    ### 1 - Left Click 
            if event.type == pygame.MOUSEBUTTONDOWN:         ### 2 - Middle Mouse Click
                if event.button == 1:                        ### 3 - Right CLick
                    
                    if not bird_fly:
                        bird_fly = True
                        line_distance = distance(mouse, bird.body.position)
                        proj_angle = angle(mouse, bird.body.position)
                        force_x = line_distance * math.cos(proj_angle) * 6
                        force_y = line_distance * math.sin(proj_angle) * 6
                        bird.body.apply_impulse_at_local_point((force_x, force_y), (0, 0))
                                                             ### 4 - Scroll Up
                                                             ### 5 - Scroll Down
                if event.button == 3:
                    pigs.insert(pig_num,spawn_pig(8, RADIUS+5, mouse))
                    simulation.add(pigs[pig_num].body, pigs[pig_num])
                    
                    pig_num+=1
                    print("Spawned pig!")
            
       



                       

                                                            

        
        if not bird_fly:
            #print(bird.body.position)
            aim_line = [mouse, bird.body.position] 
            pygame.draw.line(display, (0,0,0), aim_line[0], aim_line[1])
        else:
            time+=1/60
            if time > 10:
                return Simulation(WIDTH, HEIGHT, RADIUS)
       
        simulation.debug_draw(options)
        simulation.step(1/60)
        clock.tick(60)
        # time+=1/60

        #update window
        pygame.display.flip()
        
        
Simulation(WIDTH, HEIGHT, RADIUS)