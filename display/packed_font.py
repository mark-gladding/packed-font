
# Module for rendering different sized fonts on the SSD1306 Pico Pi Display.
# Fonts are stored in a memory efficient binary format.
# Fonts can be proportional or monospaced.
# A font can contain just the characters needed for a specific application.
#
# Copyright (C) Mark Gladding 2023.
#
# MIT License (see the accompanying license file)
#

_loaded_fonts = {}
_current_font = None

def load_font(font_name):
    """Load a packed font into memory for use. Once loaded, the font must be selected for use.

    Args:
        font_name (string): Name of the font, without the .pf extension.
    """    
    global _loaded_fonts

    if font_name in _loaded_fonts:
        return
    _loaded_fonts[font_name] = _load_packed_font(font_name) 

def _load_packed_font(font_name):
    font = None
    with open(f'{font_name}.pf', 'rb') as f:
        header = f.read(4)    
        if len(header) < 4 or header[0] != ord('P') or header[1] != ord('F'):
            print(f'{font_name}.pf has an unknown file format')
            return
        font = {  'name' : font_name,
                  'default_character' : chr(header[2]),
                  'character_count': header[3],
                  'characters' : {},
                  'data' : None           
                }

        print(f'Reading font {font_name} with {font["character_count"]} characters.')

        remaining_header_size = font['character_count'] * 5
        header = f.read(remaining_header_size)
    
        index = 0
        characters = font['characters']
        for i in range(font["character_count"]):
            character = chr(header[index])
            index += 1
            char_width = header[index]
            index += 1
            char_height = header[index]
            index += 1
            start_index = header[index] + header[index + 1] * 256
            index += 2
            characters[character] = {
                'char_width' : char_width,
                'char_height' : char_height,
                'start_index' : start_index
            }
        font['data'] = f.read()
        return font

def unload_all_fonts():
    """ Unload all fonts and select the built in font as the current font."""
    global _loaded_fonts,  _current_font
    _loaded_fonts = {}
    _current_font = None

def select_font(font_name):
    """Select the font to use for subsequent calls to get_text_size() and text()

    Args:
        font_name (string): Name of the font to select or None to select the built in font.
    """    
    global _current_font

    if font_name == None:       # Select the built in font
        _current_font = None
        return

    if _current_font and _current_font['name'] == font_name:
        return
    
    if not font_name in _loaded_fonts:
        print(f'Cannot select unknown font {font_name}.')
        return
    _current_font = _loaded_fonts[font_name]
    

def get_text_size(text):
    """Calculate the width and height of the rendered text using the currently selected font.

    Args:
        text (string): The text string to measure

    Returns:
        (int, int): Tuple containing the width and height of the rendered text.
    """
    if not _current_font:
        return len(text) * 8, 8     # Built in font
    
    characters = _current_font['characters']
    default_character = _current_font['default_character']
    width = 0
    height = 0
    for char in text:
        try:
            char_definition = characters[char]
        except KeyError:
            char_definition = characters[default_character]
        width += char_definition['char_width']
        height = max(height, char_definition['char_height'])
    return width, height

def text(display, text, x, y, max_width=0, horiz_align=0, max_height=0, vert_align=0, c=1):
    """Render a text string to the display in the currently selected font, with optional alignment.

    Args:
        display (PiicoDev_SSD): The display to render the text on
        text (string): Text to render
        x (int): X coordinate to begin text rendering
        y (int): Y coordinate to begin text rendering
        max_width (int, optional): Width of the box to align text horizontally within. Defaults to 0.
        horiz_align (int, optional): 0 = Left, 1 = Center, 2 = Right. Defaults to 0.
        max_height (int, optional): Height of the box to align text vertically within. Defaults to 0.
        vert_align (int, optional): 0 = Top, 1 = Center, 2 = Bottom. Defaults to 0.
        c (int, optional): Color to render text in. Defaults to 1.
    """    
    
    if (max_width > 0 and horiz_align > 0) or (max_height > 0 and vert_align > 0):
        total_text_width, text_height = get_text_size(text)
        if horiz_align == 1:     # Center
            x += int((max_width - total_text_width) / 2)
        elif horiz_align == 2:   # Right
            x += max_width - total_text_width
        if vert_align == 1:      # Center
            y += int((max_height - text_height) / 2)
        elif vert_align == 2:    # Bottom
            y += max_height - text_height

    if not _current_font:   # Built in font
        display.text(text, x, y, c)
        return
    
    characters = _current_font['characters']
    default_character = _current_font['default_character']
    data = _current_font['data']
    for char in text:
        try:
            char_definition = characters[char]
        except KeyError:
            char_definition = characters[default_character]
        start_index = char_definition['start_index']
        width = char_definition['char_width']
        height = char_definition['char_height']
        width_in_bytes = int((width + 7) / 8)
        for i in range(height):
            for j in range(width):
                byte_index = int(j / 8)
                bit_index = j - byte_index * 8
                val = data[start_index + i * width_in_bytes + byte_index ]
                if (val >> (7-bit_index)) & 1:
                    display.pixel(x + j, y + i, c)
        x += width
