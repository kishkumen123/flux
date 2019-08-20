from flux import Flux

engine = Flux()
engine.init()

display = engine.init_display((800, 600))


background = engine.create_surface((100, 100), (200, 255, 255))

poly = engine.create_poly((50, 150, 50), ((100, 100), (40, 40), (60, 60), (200, 100), (200, 200), (100, 200)), fill=True)
poly.move_point_on_press()

engine.set_fps(120)
while engine.is_running():
    display.clear_screen()
    engine.update()

    for event in engine.events.get():
        if engine.events.QUIT(event):
            engine.kill()
        elif engine.events.KEYDOWN(event):
            if engine.key.is_ESCAPE(event):
                engine.kill()
        elif engine.events.RESIZE(event):
            display.resize(event.dict["size"])

    #display.load_to_buffer(background)
    poly.draw(engine.mouse_rect)
    #engine.draw_poly((50, 150, 50), ((100, 100), (40, 40), (60, 60), (200, 100), (200, 200), (100, 200)), fill=True)

    display.swap_buffer()
engine.quit()



# display.set_caption(text)
# text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(engine.get_fps(), engine.elapsed_time)
