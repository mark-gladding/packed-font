from PiicoDev_SSD1306 import *
import machine
import math
import time
import packed_font
import struct

_display = None

def init_display():
    global _display

    _display = create_PiicoDev_SSD1306()
    if _display.comms_err:
        print('Display not detected.')
        _display = None
    else:
        for font_name in ['digits-30', 'text-16', 'icons-32', 'icons-128']:
            packed_font.load_font(font_name)

def is_present():
    return _display != None 

def clear():
    if not _display:
        return
    
    _display.fill(0)
    _display.show()

def _title(text):
    isTitlePos = True
    base = ord('A')
    offset = -ord('a')
    titleText = ''
    for c in text:
        if(isTitlePos and c >= 'a' and c <= 'z'):
            titleText += (chr(ord(c) + offset + base))
            isTitlePos = False
        else:
            if c == ' ':
                isTitlePos = True
            titleText += c
    return titleText

def save_screenshot(filename):

    rows = []
    for y in range(64):
        ybit = y % 8
        row = []
        for x in range(128 // 8):
            val = 0
            for b in range(8):
                yval = _display.buffer[(y // 8) * 128 + x * 8 + b]
                val += (1 << (7-b)) if ((yval >> ybit) & 1) == 1 else 0

            row.append(val)
        rows.append(row)

    data = bmp(rows, 128)
    with open(filename, "wb") as f:
        f.write(data)
    


def bmp(rows, w):

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



def run_demo_loop():
    if not _display:
        return

    packed_font.select_font('icons-128')
    packed_font.text(_display, 's', 0, 0)
    packed_font.select_font('text-16')
    packed_font.text(_display, 'Welcome', 0, 0, 128, 1, 64, 1)

    save_screenshot("title.bmp")

    _display.show()
    return
    time.sleep(3)

    _display.fill(0)

    packed_font.text(_display, 'Text', 0, 16, 128, 1)
    packed_font.text(_display, 'Alignment', 0, 32, 128, 1)

    _display.show()
    time.sleep(1)

    _display.fill(0)

    packed_font.text(_display, 'left, top', 0, 0, 128, 0, 64, 0)
    packed_font.text(_display, 'left, center', 0, 0, 128, 0, 64, 1)
    packed_font.text(_display, 'left, bottom', 0, 0, 128, 0, 64, 2)

    _display.show()
    time.sleep(2)

    _display.fill(0)

    packed_font.text(_display, 'center, top', 0, 0, 128, 1, 64, 0)
    packed_font.text(_display, 'center, center', 0, 0, 128, 1, 64, 1)
    packed_font.text(_display, 'center, bottom', 0, 0, 128, 1, 64, 2)

    _display.show()
    time.sleep(2)

    _display.fill(0)

    packed_font.text(_display, 'right, top', 0, 0, 128, 2, 64, 0)
    packed_font.text(_display, 'right, center', 0, 0, 128, 2, 64, 1)
    packed_font.text(_display, 'right, bottom', 0, 0, 128, 2, 64, 2)

    _display.show()
    time.sleep(2)

    _display.fill(0)

    packed_font.text(_display, 'Text +', 0, 16, 128, 1)
    packed_font.text(_display, 'Icons', 0, 32, 128, 1)

    _display.show()
    time.sleep(1.5)

    _display.fill(0)

    packed_font.select_font('digits-30')
    degrees = '\u00b0'
    packed_font.text(_display, f'12.3{degrees}', 0, 0, 128, 1, 64, 1)
    packed_font.select_font('icons-32')
    packed_font.text(_display, f't', 0, 0, 128, 2)

    _display.show()
    time.sleep(2)

    _display.fill(0)

    packed_font.select_font('digits-30')
    packed_font.text(_display, f'76', 0, 0, 128, 1, 64, 1)
    packed_font.select_font('icons-32')
    packed_font.text(_display, f'h', 0, 0, 128, 2)

    _display.show()
    time.sleep(2)    

    _display.fill(0)

    packed_font.select_font('digits-30')
    packed_font.text(_display, f'985', 0, 0, 128, 1, 64, 1)
    packed_font.select_font('icons-32')
    packed_font.text(_display, f'p', 0, 0, 128, 2)

    _display.show()
    time.sleep(2)