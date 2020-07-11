
if __name__ == "__main__":
    from flux.main import Flux
    from components import components_list
    from systems import RenderSystem, ScaleSprite, TranslateSprite

    engine = Flux()
    engine.init()
    engine.register_components(components_list)
    engine.init_groups("resources/data/groups.json")
    engine.load_entities("resources/data/entities.json")

    display = engine.init_display((1280, 720))
    background = engine.create_surface((100, 100), (200, 255, 255))
    engine.set_fps(120)

    #engine.load_level("one")

    while engine.is_running():
        #RenderSystem.update()
        #RenderSystem.draw(display.fake_display)
        #TranslateSprite.update(engine.delta_time)
        #ScaleSprite.update(engine.delta_time)

        #if engine.button_released("M_LEFT", "layer_all"):
            #print("M_LEFT - released")
        if engine.button_pressed_once("M_LEFT", "layer_all"):
            print("M_LEFT - pressed once")
        #if engine.button_pressed("M_LEFT", "layer_all"):
        #    print("M_LEFT - pressed")
        #if engine.button_pressed("M_RIGHT", "layer_all"):
        #    print("M_RIGHT - pressed")
        #if engine.button_pressed("M_MIDDLE", "layer_all"):
        #    print("M_MIDDLE - pressed")
        #if engine.button_pressed("M_SCROLLDOWN", "layer_all"):
        #    print("M_SCROLLDOWN - pressed")
        #if engine.button_pressed("M_SCROLLUP", "layer_all"):
        #    print("M_SCROLLUP - pressed")

        if engine.key_pressed("K_ESCAPE", "layer_all"):
            engine.kill()
        if engine.event_triggered("QUIT", "layer_all"):
            engine.kill()

        engine.flush()
        display.swap_buffer()
        display.clear_screen()
        engine.update()

    engine.quit()
