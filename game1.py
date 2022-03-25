import pygame
import pymunk
import pymunk.pygame_util
import math


pygame.init()
WIDTH, HEIGHT = 1300, 900

# colors
WHITE = (255, 255, 255)


window = pygame.display.set_mode((WIDTH, HEIGHT))

def calulate_distance(p1, p2):
    distance = math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[1])**2)
    return distance

def calculate_angle(p1, p2):
    angle = math.atan2(p2[1] - p1[1], p2[0] - p1[0])
    return angle

def create_boundaries(space, width, height):
    rects = [
        [(width/2, height -10), (width, 20)],
        [(width/2, 10), (width, 20)],
        [(10, height/2), (20, height)],
        [(width - 10, height/2), (20, height)]
        ]
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)

def create_ball(space, radius, mass):
    body = pymunk.Body()
    body.position = (WIDTH / 2, 100)

    ball = pymunk.Circle(body, radius)
    ball.mass = mass
    ball.color = (255, 255, 0, 100)
    ball.elasticity = 0.9
    ball.friction = 0.5
    space.add(body, ball)
    return ball

def draw(space, window, draw_options):
    window.fill(WHITE)
    space.debug_draw(draw_options)
    pygame.display.update()


def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1 / fps  # delta time for simulations

    # draw simulation
    space = pymunk.Space()
    space.gravity = (0, 981)
    draw_options = pymunk.pygame_util.DrawOptions(window)

    # create objects
    ball = create_ball(space, 30, 10)
    create_boundaries(space, width, height)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                ball.body.apply_impulse_at_local_point((10000,0), (0,0))


        draw(space, window, draw_options)
        

        space.step(dt)
        clock.tick(fps)

        


    pygame.quit()

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)
