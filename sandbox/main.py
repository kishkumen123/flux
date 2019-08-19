from flux import Flux

engine = Flux()
engine.init()

display = engine.init_display((800, 600))


background = engine.create_surface((800, 600), (200, 255, 255))
display.load_to_buffer(background)

engine.set_fps(120)
while engine.is_running():

    for event in engine.events.get():
        if engine.events.QUIT(event):
            engine.kill()
        elif engine.events.KEYDOWN(event):
            if engine.key.is_ESCAPE(event):
                engine.kill()
        elif engine.events.RESIZE(event):
            display.resize(event.dict["size"])

    display.clear_screen()
    display.load_to_buffer(background)
    display.swap_buffer()
    text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(engine.get_fps(), engine.elapsed_time)
    display.set_caption(text)

engine.quit()
