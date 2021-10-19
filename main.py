import pygame, sys, os
from random        import randint
from Entity        import Entity
from EntityManager import EntityManager
from Systems       import ControlSystem, ParticleSystem
from World         import World
from text          import create_fonts, render, display_fps

# <>
# class Attributes(dict):
#     def __init__(self, **kwargs):
#         super().__init__(**kwargs)
#
#     def __getattr__(self, attribute):
#         return self[attribute]
#
#     def __repr__(self):
#         str_text = 'Attributes('
#         for j, att in enumerate(self.items()):
#             str_text += f'{att[0]}={repr(att[1])}'
#             if j != len(self) - 1:
#                 str_text += ','
#         str_text += ')'
#         return str_text
# </>

# Simple color access ----------------------------------------------------------
WHITE   = (255,255,255)
CYAN    = (  0,255,255)
BLUE    = (  0,  0,255)
MAGENTA = (255,  0,255)
RED     = (255,  0,  0)
YELLOW  = (255,255,  0)
BLACK   = (  0,  0,  0)


# Initialize pygame ------------------------------------------------------------
pygame.init()

# os.system('cls')





id = '-1'
def next_id():
    global id
    id = str(int(id)+1)
    return id







screen = pygame.display.set_mode((500, 500),pygame.DOUBLEBUF)
clock  = pygame.time.Clock()
fonts  = create_fonts([32,16,14,8])
pygame.event.set_allowed([pygame.QUIT,pygame.KEYDOWN,pygame.KEYUP])

# Initialize Entity Component System -------------------------------------------
em    = EntityManager()
world = World(ControlSystem  = ControlSystem (em),
              ParticleSystem = ParticleSystem(em, screen))

em[next_id()] = Entity(ControllerComponent = {},
                     SpriteComponent     = 'player.png',
                     PositionComponent   = {'x':0,'y':0},
                     VelocityComponent   = {'x':0,'y':0},
                     DirectionComponent  = {'x':0,'y':0},
                    )

# Begin main game loop ---------------------------------------------------------
while 1:
    # Mouse variable for easy access -------------------------------------------
    mouse = pygame.mouse.get_pos()

    # Delta Time variable ------------------------------------------------------
    dt = clock.get_time()/1000.0

    # Reset screen -------------------------------------------------------------
    screen.fill(BLACK)

    # Write the fps and entity count on screen ---------------------------------
    render(fonts[0], str(len(em)), 'white', (250,0), screen)
    display_fps(fonts[0], clock, screen)


    em[next_id()]=Entity(PositionComponent = {'x':250,'y':250},
                         VelocityComponent = {'x':randint(-360,360)/180,'y':randint(-360,360)/180},
                         ParticleComponent = True,
                         TimerComponent    = {'timer':5, 'time':.1})



    # Update every system ------------------------------------------------------
    world.update(dt)

    # Handle pygame events -----------------------------------------------------
    for e in pygame.event.get():
        if e.type == pygame.QUIT or \
          (e.type == pygame.KEYDOWN and e.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()

    # Update and tick screen ---------------------------------------------------
    pygame.display.update()
    clock.tick(60)
