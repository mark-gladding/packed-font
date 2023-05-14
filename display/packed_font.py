
_loaded_fonts = {}
_current_font = None

def load_font(font_name):
    global _loaded_fonts

    if font_name in _loaded_fonts:
        return
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
        _loaded_fonts[font_name] = font 

def unload_all_fonts():
    global _loaded_fonts
    _loaded_fonts = {}

def select_font(font_name):
    global _current_font
    if _current_font and _current_font['name'] == font_name:
        return
    
    if not font_name in _loaded_fonts:
        print(f'Cannot select unknown font {font_name}.')
        return
    _current_font = _loaded_fonts[font_name]
    

def get_text_size(text):
    if not _current_font:
        print(f'No font selected: {text}')
        return
    
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
    
    if not _current_font:
        print(f'No font selected: {text}')
        return
    
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
