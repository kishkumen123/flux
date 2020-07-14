
if __name__ == "__main__":
    import pygame
    from flux.main import Flux
    #from components import components_list
    #from systems import RenderSystem, ScaleSprite, TranslateSprite

    flux = Flux()
    flux.init()
    display = flux.get_display()
    flux.set_fps(120)

    #flux.register_components(components_list)
    #flux.init_groups("resources/data/groups.json")
    #flux.load_entities("resources/data/entities.json")

    while flux.is_running():
        #RenderSystem.update()
        #RenderSystem.draw(display)
        #TranslateSprite.update(flux.dt)
        #ScaleSprite.update(flux.dt)
        
        if flux.key_pressed("K_ESCAPE", "layer_all"):
            flux.quit()
        
        pygame.display.update()
        display.fill((0, 0, 0))
        flux.update()

    flux.quit()
