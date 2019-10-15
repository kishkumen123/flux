from flux import Flux

engine = Flux()
engine.init()

display = engine.init_display((800, 600))


background = engine.create_surface((100, 100), (200, 255, 255))

engine.create_poly("one", "layer_0", (50, 150, 50), ((100, 100), (150, 50), (200, 100), (200, 150), (150, 200), (100, 150)))
engine.create_poly("two", "layer_0", (50, 50, 150), ((200, 200), (250, 150), (300, 200), (300, 250), (250, 300), (200, 250)))
engine.create_poly("three", "layer_0", (150, 50, 50), ((300, 300), (350, 250), (400, 300), (400, 350), (350, 400), (300, 350)))
engine.create_poly("four", "layer_0", (50, 150, 50), ((100, 100), (150, 50), (200, 100), (200, 150), (150, 200), (100, 150)))
engine.create_poly("five", "layer_0", (50, 50, 150), ((200, 200), (250, 150), (300, 200), (300, 250), (250, 300), (200, 250)))
engine.create_poly("six", "layer_0", (150, 50, 50), ((300, 300), (350, 250), (400, 300), (400, 350), (350, 400), (300, 350)))
engine.create_poly("seven", "layer_0", (50, 150, 50), ((100, 100), (150, 50), (200, 100), (200, 150), (150, 200), (100, 150)))
engine.create_poly("eight", "layer_0", (50, 50, 150), ((200, 200), (250, 150), (300, 200), (300, 250), (250, 300), (200, 250)))
engine.create_poly("nine", "layer_0", (150, 50, 50), ((300, 300), (350, 250), (400, 300), (400, 350), (350, 400), (300, 350)))
engine.create_poly("nine", "layer_0", (200, 200, 200), ((300, 300), (350, 250), (400, 300), (400, 350), (350, 400), (300, 350)))
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
