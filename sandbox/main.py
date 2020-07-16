#
#if __name__ == "__main__":
#    import sys
#    import pygame
#    from pygame.locals import *
#
#    from flux.main import Flux
#    #from components import components_list
#    #from systems import RenderSystem, ScaleSprite, TranslateSprite
#
#    flux = Flux()
#    #flux.init()
#    #display = flux.get_display()
#    flux.set_fps(120)
#
#    pygame.init()
#    fps = 60
#    fpsClock = pygame.time.Clock()
#    flux.display(pygame.display.set_mode((1024, 720)))
#
#    #flux.register_components(components_list)
#    #flux.init_groups("resources/data/groups.json")
#    #flux.load_entities("resources/data/entities.json")
#
#    while flux.is_running():
#
#        if pygame.event.peek(pygame.KEYDOWN):
#            print("OK")
#            event = pygame.event.get(pygame.KEYDOWN)[0]
#            print(event)
#            if event.key == K_ESCAPE:
#                pygame.quit()
#                sys.exit(0)
#            if event.type == QUIT:
#                pygame.quit()
#                sys.exit(0)
#
#        #RenderSystem.update()
#        #RenderSystem.draw(display)
#        #TranslateSprite.update(flux.dt)
#        #ScaleSprite.update(flux.dt)
#        
#        #if flux.key_pressed("K_ESCAPE", "layer_all"):
#            #flux.quit()
#
#        if flux.key_repeat("K_w", "layer_all"):
#            print("w")
#
#        #text = flux.text_input_repeat("layer_0")
#        #if text:
#            #print(text)
#        
#        flux.update()
#        pygame.event.get()
#        pygame.display.update()
#        display.fill((0, 0, 0))

if __name__ == "__main__":
    import sys
     
    import pygame
    from pygame.locals import *
    from console import C, CState
     
    pygame.init()
     
    fps = 60
    clock = pygame.time.Clock()
     
    width, height = 1024, 720
    screen = pygame.display.set_mode((width, height))

    c = C(screen)
     

    while True:
        dt = clock.tick(60) / 1000
        screen.fill((0, 0, 0))

        if pygame.event.peek(QUIT):
            pygame.quit()
            sys.exit(0)

        if c.state == CState.CLOSED:
            if pygame.event.peek(KEYDOWN):
                event = pygame.event.get(pygame.KEYDOWN)[0]
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit(0)
                if event.key == K_BACKQUOTE and not event.mod:
                    c.open(CState.OPEN_SMALL)
                if event.key == K_BACKQUOTE and event.mod:
                    c.open(CState.OPEN_BIG)

        c.update(dt)
        pygame.event.get()
        pygame.display.flip()
        clock.tick(fps)
