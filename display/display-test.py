from enhanced_display import Enhanced_Display
import time

if __name__ == "__main__":

    display = Enhanced_Display()
    display.load_fonts(['digits-30', 'text-16', 'icons-32', 'icons-128'])

    display.clear()

    display.select_font('text-16')
    display.text('2D Drawing', 0, 0, 1, 1)

    display.show()
    time.sleep(1)    

    display.fill(0)
    display.pixel(64, 10, 1)
    display.pixel(65, 10, 1)
    display.pixel(66, 10, 1)

    display.line(0, 0, display.width -1, display.height -1, 1)
    display.line(display.width -1, 0, 0, display.height -1, 1)

    display.hline(0, 8, display.width, 1)
    display.hline(0, 48, display.width, 1)

    display.vline(8, 0, display.height, 1)
    display.vline(120, 0, display.height, 1)

    display.rect(0, 0, display.width, display.height, 1)

    display.fill_rect(16, 2, 96, 2, 1)

    display.circ(display.width // 2, display.height // 2, 16, 0)
    display.arc(display.width // 2, display.height // 2, 24, 45, 90)

    display.show()

    time.sleep(1)
    display.invert(1)
    time.sleep(1)
    display.setContrast(0)
    time.sleep(1)
    display.setContrast(128)
    time.sleep(1)
    display.setContrast(255)
    time.sleep(1)
    display.invert(0)
    time.sleep(1)
    display.rotate(False)
    time.sleep(1)
    display.rotate(True)
    time.sleep(1)

    for i in range(16):
        display.scroll(8, 4)
        display.fill_rect(0, 0, display.width, 4, 0)
        display.fill_rect(0, 4, 8, display.height - 4, 0)
        display.show()
    

