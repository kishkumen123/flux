from flux import Flux

engine = Flux()
engine.init()

display = engine.init_display((1800, 1600))


background = engine.create_surface((100, 100), (200, 255, 255))

poly = engine.create_poly((50, 150, 50), ((100, 100), (40, 40), (60, 60), (200, 100), (200, 200), (100, 200)))
poly.editable()
poly.wireframe()

engine.set_fps(120)

while engine.is_running():
    display.clear_screen()

    if engine.key_pressed("BACKSPACE"): print("OK")
    if engine.key_pressed("ESCAPE"): engine.kill()
    if engine.event_active("QUIT"): engine.kill()

    # this needs to go away, mouse needs to be like key and events, and event has the freaking mouse buttons right now and those needs to be moved to Mouse class
    poly.draw()

    engine.update()
    display.swap_buffer()

engine.quit()



# display.set_caption(text)
# text = "FPS: {0:.2f}   Playtime: {1:.2f}".format(engine.get_fps(), engine.elapsed_time)
