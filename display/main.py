from enhanced_display import Enhanced_Display
import time

if __name__ == "__main__":

    display = Enhanced_Display()
    display.load_fonts(['digits-30', 'text-16', 'icons-32', 'icons-128'])

    display.select_font('icons-128')
    display.text('s', 0, 0)
    display.select_font('text-16')
    display.text('Welcome', 0, 0, 1, 1)

    display.save_screenshot("title.bmp")

    display.show()

    time.sleep(3)

    display.fill(0)

    display.text('Text', 0, 16, 1)
    display.text('Alignment', 0, 32, 1)

    display.show()
    time.sleep(1)

    display.fill(0)

    display.text('left, top', 0, 0)
    display.text('left, center', 0, 0, 0, 1)
    display.text('left, bottom', 0, 0, 0, 2)

    display.show()
    time.sleep(2)

    display.fill(0)

    display.text('center, top', 0, 0, 1, 0)
    display.text('center, center', 0, 0, 1, 1)
    display.text('center, bottom', 0, 0, 1, 2)

    display.show()
    time.sleep(2)

    display.fill(0)

    display.text('right, top', 0, 0, 2, 0)
    display.text('right, center', 0, 0, 2, 1)
    display.text('right, bottom', 0, 0, 2, 2)

    display.show()
    time.sleep(2)

    display.fill(0)

    display.text('Text', 0, 8, 1)
    display.text('&', 0, 24, 1)
    display.text('Icons', 0, 40, 1)

    display.show()
    time.sleep(1.5)

    display.fill(0)

    display.select_font('digits-30')
    degrees = '\u00b0'
    display.text(f'12.3{degrees}', 0, 0, 1, 1)
    display.select_font('icons-32')
    display.text(f't', 0, 0, 2)

    display.show()
    time.sleep(2)

    display.fill(0)

    display.select_font('digits-30')
    display.text(f'76', 0, 0, 1, 1)
    display.select_font('icons-32')
    display.text(f'h', 0, 0, 2)

    display.show()
    time.sleep(2)    

    display.fill(0)

    display.select_font('digits-30')
    display.text(f'985', 0, 0, 1, 1, display.width - 32)
    display.select_font('icons-32')
    display.text(f'p', 0, 0, 2)

    display.show()
    time.sleep(2)