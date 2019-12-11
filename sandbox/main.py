
if __name__ == "__main__":
    from flux import Flux

    engine = Flux()
    engine.init()

    display = engine.init_display((1280, 720))
    background = engine.create_surface((100, 100), (200, 255, 255))
    engine.set_fps(120)

    player = engine.create_player()

    height_map = [
        ((66, 167, 245), -0.8),
        ((66, 105, 245), -0.5),
        ((222, 219, 149), -0.3),
        ((15, 209, 54), 0.2),
        ((13, 145, 40), 0.3),
        ((99, 81, 7), 0.4),
        ((61, 50, 4), 0.5),
        ((232, 232, 230), 1)
    ]

    #world = engine.generate_world(color_height_map=height_map)
    world = engine.generate_world()
    move_speed = 0.7

    while engine.is_running():
        display.clear_screen()

        if engine.key_pressed("a", "layer_0"):
            world.move(x=-move_speed)
        if engine.key_pressed("d", "layer_0"):
            world.move(x=move_speed)
        if engine.key_pressed("w", "layer_0"):
            world.move(y=-move_speed)
        if engine.key_pressed("s", "layer_0"):
            world.move(y=move_speed)

        if engine.key_pressed("ESCAPE", "layer_0"):
            engine.kill()
        if engine.event_triggered("QUIT"):
            engine.kill()


        world.update()
        #engine.draw_poly()
        engine.update()
        display.swap_buffer()

    engine.quit()
