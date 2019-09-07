from flux import Flux

engine = Flux()
engine.init()

display = engine.init_display((800, 600))


background = engine.create_surface((100, 100), (200, 255, 255))

poly = engine.create_poly((50, 150, 50), ((100, 100), (40, 40), (60, 60), (200, 100), (200, 200), (100, 200)))
poly.editable()
#poly.wireframe()

engine.set_fps(120)

while engine.is_running():
    display.clear_screen()

    if engine.key_pressed("ESCAPE", "layer_0"):
        engine.kill()
    if engine.event_triggered("QUIT"):
        engine.kill()

    poly.draw()

    engine.update()
    display.swap_buffer()

engine.quit()
