
if __name__ == "__main__":
    from flux.main import Flux

    engine = Flux()
    engine.init()

    engine.renderer.create_sprite_group("group1")

    engine.renderer.create_sprite("group1", 0, "red.jpg", 100, 100)
    engine.renderer.create_sprite("group1", 1, "yellow.jpg", 110, 110)
    engine.renderer.create_sprite("group1", 0, "blue.jpg", 120, 120)
    engine.renderer.create_sprite("group1", 3, "white.jpg", 130, 130)
    engine.renderer.create_sprite("group1", 2, "purple.jpg", 140, 140)

    engine.renderer.create_sprite("group1", 0, "red.jpg", 200, 200)
    engine.renderer.create_sprite("group1", 1, "yellow.jpg", 210, 210)
    engine.renderer.create_sprite("group1", 3, "blue.jpg", 220, 220)
    engine.renderer.create_sprite("group1", 4, "white.jpg", 230, 230)
    engine.renderer.create_sprite("group1", 5, "purple.jpg", 240, 240)

    #engine.ui.create_panel("panel1", size=[300, 500], position=[150, 150], debug=True, _layer="layer_1", show=True)
    #engine.ui.create_button("button1", parent="panel1", size=[100, 50])
    #engine.ui.create_slider("slider1", parent="panel1", size=[100, 15], sl_range=[0, 5], starting_value=5, _round=True)
    #engine.ui.create_button("button2", parent="panel1", size=[100, 50])
    #engine.ui.create_slider("slider2", parent="panel1", size=[100, 15], sl_range=[0, 5], starting_value=2)
    #engine.ui.create_slider("slider3", parent="panel1", size=[100, 15], sl_range=[0, 5], starting_value=4)

    display = engine.init_display((1280, 720))
    background = engine.create_surface((100, 100), (200, 255, 255))
    engine.set_fps(120)

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

    #world = engine.generate_world(scale=40, color_height_map=height_map)
    #world = engine.generate_world()
    move_speed = 0.7
    engine.load_level("one")

    while engine.is_running():

        if engine.key_pressed_once("TAB", "layer_all"):
            engine.ui.toggle_panel("panel1")

        #if engine.key_pressed("a", "layer_0"):
        #    world.move(x=-move_speed)
        #if engine.key_pressed("d", "layer_0"):
        #    world.move(x=move_speed)
    #if engine.key_pressed("w", "layer_0"):
        #    world.move(y=-move_speed)
        #if engine.key_pressed("s", "layer_0"):
        #    world.move(y=move_speed)

        if engine.key_pressed("ESCAPE", "layer_all"):
            engine.kill()
        if engine.event_triggered("QUIT", "layer_all"):
            engine.kill()


        #world.update()
        #engine.draw_poly()
        engine.flush()
        display.swap_buffer()
        display.clear_screen()
        engine.update()

    engine.quit()
