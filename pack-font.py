import argparse
import json
from PIL import Image
import os
import sys

def len_in_bytes(pixels):
    return int((pixels + 7) / 8)

def create_packed_font(font_info_filename, verbose):
    with open(font_info_filename) as f:
        font_info = json.load(f)

    name = font_info["Name"]
    default_width = font_info["Width"]
    height = font_info["Height"]
    default_character = font_info["DefaultCharacter"]
    character_count = len(font_info["Characters"])

    print(f'Creating font {name}, size {default_width}x{height} with {character_count} characters.')

    # Packed font format
    # Header - MPF
    # Height (1 byte)
    # Default Character (1 byte)
    # Number of characters (1 byte)
    #  Character 1
    #       Character code (1 byte)
    #       Width (1 byte)
    #       YOffset (1 byte)
    #       StartIndex (2 bytes)
    #       Character data

    header = [ord('P'), ord('F'), height, ord(default_character), character_count ]
    data = []
    start_index = 0

    for character in font_info["Characters"]:
        code = character["Code"]
        width = character["Width"] if "Width" in character else default_width
        header.append(ord(code))
        header.append(width)  
        header.append(0)          # YOffset
        header.append(start_index % 256)
        header.append(start_index >> 8)

        if verbose:
            print(code)
        filename = f"{code}.bmp"
        im = Image.open(filename)
        image_width = im.size[0]
        image_height = im.size[1]
        if image_width < width or image_height < height:
            print(f'Image {filename}, size {im.size} less than expected ({width},{height})')
            sys.exit(-1)


        image_data = list(im.getdata())
        for i in range(height):
            row = image_data[i*image_width:i*image_width + image_width]
            if verbose:
                print(row)
            for b in range(len_in_bytes(width)):
                val = 0
                for c in range(8):
                    val = val + (row[b*8 + c] << (7-c))
                data.append(val)
        start_index += len_in_bytes(width) * height

    with open(name, 'wb') as f:
        f.write(bytes(header))
        f.write(bytes(data))
    print(f'Packed font {name} successfully.')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate a Packed Font file.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(dest='--verbose', help='Output each character as an array of 0s and 1s.', default=False)
    parser.add_argument(dest='fontPathname', help='The path to the json font definition file.')
    args = parser.parse_args()

    currentDir = os.path.curdir
    os.chdir(os.path.dirname(args.fontPathname))
    try:
        create_packed_font(os.path.basename(args.fontPathname), args.verbose)
    finally:
        os.chdir(currentDir)    # Ensure the current directory is restored, even when an exception is thrown


