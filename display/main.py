# Script to demonstrate the Enhanced_Display class and associated packed fonts.
#
# Copyright (C) Mark Gladding 2023.
#
# MIT License (see the accompanying license file)
#
# https://github.com/mark-gladding/packed-font
#

from enhanced_display import Enhanced_Display
import time

if __name__ == "__main__":

    display = Enhanced_Display()

    # Load the list of fonts to use
    display.load_fonts(['digits-30', 'text-16', 'icons-32', 'icons-128'])

    # Display the Welcome screen
    display.fill(0)                         # Clear the screen

    display.select_font('icons-128')
    display.text('s', 0, 0)                 # The 's' character is the Star icon
    display.select_font('text-16')
    display.text('Welcome', 0, 0, 1, 1)     # Center the text both horizontally and vertically.

    display.save_screenshot("title.bmp")    # Take a screenshot and save to file.

    display.show()
    time.sleep(3)

    # Display the Text Alignment intro screen
    display.fill(0)

    display.text('Text', 0, 16, 1)
    display.text('Alignment', 0, 32, 1)

    display.show()
    time.sleep(1)

    # Display the left aligned text screen
    display.fill(0)

    display.text('left, top', 0, 0)
    display.text('left, center', 0, 0, 0, 1)
    display.text('left, bottom', 0, 0, 0, 2)

    display.show()
    time.sleep(1)

    # Display the center aligned text screen
    display.fill(0)

    display.text('center, top', 0, 0, 1, 0)
    display.text('center, center', 0, 0, 1, 1)
    display.text('center, bottom', 0, 0, 1, 2)

    display.show()
    time.sleep(1)

    # Display the right aligned text screen
    display.fill(0)

    display.text('right, top', 0, 0, 2, 0)
    display.text('right, center', 0, 0, 2, 1)
    display.text('right, bottom', 0, 0, 2, 2)

    display.show()
    time.sleep(1)

    # Display the Text & Icons intro screen
    display.fill(0)

    display.text('Text', 0, 8, 1)
    display.text('&', 0, 24, 1)
    display.text('Icons', 0, 40, 1)

    display.show()
    time.sleep(1.5)

    # Display the Temperature screen
    display.fill(0)

    display.select_font('digits-30')
    degrees = '\u00b0'  # Character code for the degrees symbol
    display.text(f'12.3{degrees}', 0, 0, 1, 1)
    display.select_font('icons-32')
    display.text('t', 0, 0, 2)          # The 't' character contains the temperature icon
    display.select_font(None)           # Select the built in 8 pixel font
    display.text('Temperature', 0, 0, 1, 2)

    display.show()
    time.sleep(2)

    # Display the Humidity screen
    display.fill(0)

    display.select_font('digits-30')
    display.text('76', 0, 0, 1, 1)
    display.select_font('icons-32')
    display.text('h', 0, 0, 2)          # The 'h' character contains the humidity icon
    display.select_font(None)
    display.text('Humidity', 0, 0, 1, 2)

    display.show()
    time.sleep(2)    

    # Display the Pressure screen
    display.fill(0)

    display.select_font('digits-30')
    display.text('985', 0, 0, 1, 1, display.width - 32)
    display.select_font('icons-32')
    display.text('p', 0, 0, 2)          # The 'p' character contains the pressure icon
    display.select_font(None)
    display.text('Pressure', 0, 0, 1, 2)

    display.show()
    time.sleep(2)

    # Display the Thank you screen
    display.fill(0)

    display.select_font('icons-128')
    display.text('s', 0, 0)
    display.select_font('text-16')
    display.text('Thank you', 0, 0, 1, 1)
    display.show()
