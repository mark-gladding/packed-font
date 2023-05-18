# Class used to render onto a SSD1306 Pico Pi Display with the following enhancements:
#  - Render different sized fonts using the packed_font module.
#  - Detects if a display is present and performs NOPs if not present (i.e. code will still run without a display connected)
#  - Take a screenshot of the display and save it to a .bmp file.
#
# Copyright (C) Mark Gladding 2023.
#
# MIT License (see the accompanying license file)
#
# https://github.com/mark-gladding/packed-font
#

from PiicoDev_SSD1306 import *
import math
import packed_font
import struct

class Enhanced_Display:
    def __init__(self, address=0x3C,bus=None, freq=None, sda=None, scl=None, asw=None):
        self._display = create_PiicoDev_SSD1306(address, bus, freq, sda, scl, asw)
        self.width = WIDTH
        self.height = HEIGHT
        self.is_present = False
        self.selected_font = None

        if self._display.comms_err:
            print('Display not detected.')
            self._display = None
        else:
            self.is_present = True
            print(f'Detected display of size {self.width} x {self.height} pixels.')

    # --------------- Enhanced functions --------------

    def load_font(self, font_name):
        """Load a packed font into memory for use. Once loaded, the font must be selected for use.

        Args:
            font_name (string): Name of the font, without the .pf extension.
        """    
        if self.is_present:
            packed_font.load_font(font_name)

    def load_fonts(self, font_name_list):
        """Load a list of packed fonts into memory for use. Once loaded, a font must be selected for use.

        Args:
            font_name_list (list[string]): A list of font names (without the .pf extension) to load.
        """        
        if self.is_present:
            for font_name in font_name_list:
                packed_font.load_font(font_name)        

    def unload_all_fonts(self):
        """ Unload all fonts and select the built in font as the current font."""
        if self.is_present:
            packed_font.unload_all_fonts()
            self.selected_font = None

    def select_font(self, font_name):
        """Select the font to use for subsequent calls to get_text_size() and text()

        Args:
            font_name (string): Name of the font to select or None to select the built in font.
        """    
        self.selected_font = font_name

    def get_text_size(self, text):
        """Calculate the width and height of the rendered text using the currently selected font.

        Args:
            text (string): The text string to measure

        Returns:
            (int, int): Tuple containing the width and height of the rendered text.
        """

        if self.is_present:
            packed_font.select_font(self.selected_font)
            return packed_font.get_text_size(text)
        return 0, 0
        
    def text(self, text, x, y, horiz_align=0, vert_align=0, max_width=WIDTH, max_height=HEIGHT, c=1):
        """Render a text string to the display in the currently selected font, with optional alignment.

        Args:
            text (string): Text to render.  
            x (int): X coordinate to begin text rendering.  
            y (int): Y coordinate to begin text rendering.
            horiz_align (int, optional): 0 = Left, 1 = Center, 2 = Right. Defaults to 0.
            vert_align (int, optional): 0 = Top, 1 = Center, 2 = Bottom. Defaults to 0.
            max_width (int, optional): Width of the box to align text horizontally within. Defaults to display width.
            max_height (int, optional): Height of the box to align text vertically within. Defaults to display height.
            c (int, optional): Color to render text in. Defaults to 1.
        """    
        if self.is_present:
            packed_font.select_font(self.selected_font)
            packed_font.text(self._display, text, x, y, max_width, horiz_align, max_height, vert_align, c)

    def clear(self):
        """Clear the display and show the blank screen.
        """        
        if self.is_present:
            self._display.fill(0)
            self._display.show()

    def save_screenshot(self, filename):
        """Save the current screen contents to file in .bmp format.

        Args:
            filename (string): The name of the file to save the screenshot to (e.g. screenshot.bmp)
        """        
        if self.is_present:
        
            # Rotate display buffer bytes into rows of bytes
            rows = []
            for y in range(self.height):
                ybit = y % 8
                row = []
                for x in range(self.width // 8):
                    val = 0
                    for b in range(8):
                        yval = self._display.buffer[(y // 8) * self.width + x * 8 + b]
                        val += (1 << (7-b)) if ((yval >> ybit) & 1) == 1 else 0

                    row.append(val)
                rows.append(row)

            # Convert the rows to a .bmp blob
            data = self._bmp(rows, self.width)
            # Write the blob to file.
            with open(filename, "wb") as f:
                f.write(data)

    def _bmp(self, rows, width):
        """ Create a bitmap blob from a list of rows, each row containing a list of bytes.
            Code from https://stackoverflow.com/questions/8729459/how-do-i-create-a-bmp-file-with-pure-python
        """

        mult4 = lambda n: int(math.ceil(n/4))*4
        mult8 = lambda n: int(math.ceil(n/8))*8
        lh = lambda n: struct.pack("<h", n)
        li = lambda n: struct.pack("<i", n)

        h, wB = len(rows), int(mult8(width)/8)
        s, pad = li(mult4(wB)*h+0x20), [0]*(mult4(wB)-wB)
        s = li(mult4(width)*h+0x20)
        return (b"BM" + s + b"\x00\x00\x00\x00\x20\x00\x00\x00\x0C\x00\x00\x00" +
                lh(width) + lh(h) + b"\x01\x00\x01\x00\x00\x00\x00\xff\xff\xff" +
                b"".join([bytes(row+pad) for row in reversed(rows)]))
    
    # --------------- Frame buffer functions --------------

    def fill(self, c=0):
        if self.is_present:
            self._display.fill(c)

    def pixel(self, x, y, color):
        if self.is_present:
            self._display.pixel(x, y, color)

    def line(self, x1, y1, x2, y2, c):
        if self.is_present:
            self._display.line(x1, y1, x2, y2, c)

    def hline(self, x, y, l, c):
        if self.is_present:
            self._display.hline(x, y, l, c)

    def vline(self, x, y, h, c):
        if self.is_present:
            self._display.vline(x, y, h, c)

    def rect(self, x, y, w, h, c):
        if self.is_present:
            self._display.rect(x, y, w, h, c)

    def fill_rect(self, x, y, w, h, c):
        if self.is_present:
            self._display.fill_rect(x, y, w, h, c)

    def scroll(self, xstep, ystep):
        if self.is_present:
            self._display.scroll(xstep, ystep)

    # --------------- SSD1306 display functions --------------

    def show(self):
        if self.is_present:
            self._display.show()

    def poweroff(self):
        if self.is_present:
            self._display.poweroff()

    def poweron(self):
        if self.is_present:
            self._display.poweron()

    def setContrast(self, contrast):
        if self.is_present:
            self._display.setContrast(contrast)

    def invert(self, invert):
        if self.is_present:
            self._display.invert(invert)

    def rotate(self, rotate):
        if self.is_present:
            self._display.rotate(rotate)

    def circ(self,x,y,r,t=1,c=1):
        if self.is_present:
            self._display.circ(x,y,r,t,c)

    def arc(self,x,y,r,stAng,enAng,t=0,c=1):
        if self.is_present:
            self._display.arc(x,y,r,stAng,enAng,t,c)

    def load_pbm(self, filename, c):
        if self.is_present:
            self._display.load_pbm(filename,c)

    def updateGraph2D(self, graph, value):
        if self.is_present:
            self._display.updateGraph2D(graph,value)




    


