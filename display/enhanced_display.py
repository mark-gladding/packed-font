from PiicoDev_SSD1306 import *
import math
import packed_font
import struct

class Enhanced_Display:
    def __init__(self):
        self._display = create_PiicoDev_SSD1306()
        self.width = WIDTH
        self.height = HEIGHT

        if self._display.comms_err:
            print('Display not detected.')
            self._display = None
        else:
            print(f'Detected display of size {self.width} x {self.height} pixels.')

    def is_present(self):
        return self._display != None

    def load_font(self, font_name):
        packed_font.load_font(font_name)

    def load_fonts(self, font_name_list):
        for font_name in font_name_list:
            packed_font.load_font(font_name)        

    def unload_all_fonts(self):
        packed_font.unload_all_fonts()

    def select_font(self, font_name):
        packed_font.select_font(font_name)
        
    def text(self, text, x, y,  horiz_align=0, vert_align=0, max_width=WIDTH, max_height=HEIGHT, c=1):
        if not self.is_present():
            return
        packed_font.text(self._display, text, x, y, max_width, horiz_align, max_height, vert_align, c)

    def clear(self):
        if not self.is_present():
            return
        
        self._display.fill(0)
        self._display.show()

    def fill(self, c=0):
        if not self.is_present():
            return
         
        self._display.fill(c)       

    def show(self):
        if not self.is_present():
            return
         
        self._display.show()

    def save_screenshot(self, filename):
        if not self.is_present():
            return
        
        rows = []
        for y in range(64):
            ybit = y % 8
            row = []
            for x in range(128 // 8):
                val = 0
                for b in range(8):
                    yval = self._display.buffer[(y // 8) * 128 + x * 8 + b]
                    val += (1 << (7-b)) if ((yval >> ybit) & 1) == 1 else 0

                row.append(val)
            rows.append(row)

        data = self._bmp(rows, 128)
        with open(filename, "wb") as f:
            f.write(data)

    def _bmp(self, rows, w):

        mult4 = lambda n: int(math.ceil(n/4))*4
        mult8 = lambda n: int(math.ceil(n/8))*8
        lh = lambda n: struct.pack("<h", n)
        li = lambda n: struct.pack("<i", n)

        h, wB = len(rows), int(mult8(w)/8)
        s, pad = li(mult4(wB)*h+0x20), [0]*(mult4(wB)-wB)
        s = li(mult4(w)*h+0x20)
        return (b"BM" + s + b"\x00\x00\x00\x00\x20\x00\x00\x00\x0C\x00\x00\x00" +
                lh(w) + lh(h) + b"\x01\x00\x01\x00\x00\x00\x00\xff\xff\xff" +
                b"".join([bytes(row+pad) for row in reversed(rows)]))         