
if __name__ == "__main__":
    from flux.main import Flux

    engine = Flux()
    engine.init()

    engine.ui.create_panel("panel1", size=[300, 500], position=[150, 150], debug=True, layer="layer_1", show=True)
    engine.ui.create_button("button1", parent="panel1", size=[100, 50])
    engine.ui.create_button("button2", parent="panel1", size=[100, 50])
    engine.ui.create_button("button3", parent="panel1", size=[100, 50])
    engine.ui.create_slider("slider1", parent="panel1", size=[100, 15], sl_range=[0, 5], starting_value=5, _round=True)
    engine.ui.create_button("button4", parent="panel1", size=[100, 50])
    engine.ui.create_slider("slider2", parent="panel1", size=[100, 15], sl_range=[0, 5], starting_value=2)
    engine.ui.create_slider("slider3", parent="panel1", size=[100, 15], sl_range=[0, 5], starting_value=4)

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

    while engine.is_running():
        #print(engine.ui.get_component_value("panel1", "slider1"))
        if engine.ui.get_component_value("panel1", "button1"):
            print(engine.ui.get_component_value("panel1", "button1"))

        if engine.key_pressed_once("TAB", "layer_0"):
            engine.ui.toggle_panel("panel1")

        #if engine.key_pressed("a", "layer_0"):
        #    world.move(x=-move_speed)
        #if engine.key_pressed("d", "layer_0"):
        #    world.move(x=move_speed)
        #if engine.key_pressed("w", "layer_0"):
        #    world.move(y=-move_speed)
        #if engine.key_pressed("s", "layer_0"):
        #    world.move(y=move_speed)

        if engine.key_pressed("ESCAPE", "layer_0"):
            engine.kill()
        if engine.event_triggered("QUIT"):
            engine.kill()


        #world.update()
        #engine.draw_poly()
        engine.flush()
        display.swap_buffer()
        display.clear_screen()
        engine.update()

    engine.quit()
