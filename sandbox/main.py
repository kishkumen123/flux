from flux import Flux

engine = Flux()
engine.init()

display = engine.init_display((800, 600))


background = engine.create_surface((100, 100), (200, 255, 255))

engine.create_poly("one", "layer_0", (50, 150, 50), ((100, 100), (40, 40), (60, 60), (200, 100), (200, 200), (100, 200)))
engine.create_poly("two", "layer_0", (50, 20, 150), ((50, 150), (20, 20), (40, 40), (100, 50), (20, 100), (10, 10)))
engine.create_poly("three", "layer_0", (100, 20, 150), ((60, 160), (30, 30), (50, 50), (110, 60), (30, 110), (20, 20)))
#poly0.editable()
#poly0.wireframe()

engine.set_fps(120)

while engine.is_running():
    display.clear_screen()

    if engine.key_pressed("ESCAPE", "layer_0"):
        engine.kill()
    if engine.event_triggered("QUIT"):
        engine.kill()

    engine.draw_poly()

    #poly0.draw()
    #poly1.draw()

    engine.update()
    display.swap_buffer()

engine.quit()
