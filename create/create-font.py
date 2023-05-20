# Script to render a truetype font (or any font format supported by PIL) and 
# create a series of font bitmaps and an associated definition file which can then be
# used as inputs to create a packed font for use on a Pico Pi SSD1306 display.
#
# It depends on the Pillow (PIL) library, available here: https://pillow.readthedocs.io/en/stable/index.html#
#
# Copyright (C) Mark Gladding 2023.
#
# MIT License (see the accompanying license file)
#
# https://github.com/mark-gladding/packed-font
#

import argparse
import json
from PIL import Image, ImageFont, ImageDraw
import os
import sys

def len_in_bytes(pixels):
    return int((pixels + 7) / 8)

def rounded_width(pixels):
    return len_in_bytes(pixels) * 8

def ensure_folder_exists(folderName):
    folderName = os.path.normpath(folderName)
    if not folderName or os.path.exists(folderName):
        return
    head = os.path.dirname(folderName)
    ensure_folder_exists(head)
    os.mkdir(folderName)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Create a series of font bitmaps and an associated definition file.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('sourceFontPathname', help='The path to the source font file (e.g. TTF).')
    parser.add_argument('fontPathname', help='The path to the json font definition file.')
    parser.add_argument('--verbose', help='Output each character as an array of 0s and 1s.', action='store_true')
    parser.add_argument('--chars', help='Series of comma separated character ranges to include (e.g. 32-57,59,100-120).', default='32-126')
    parser.add_argument('--xoffsets', help='Series of comma separated x-offsets for specific characters (e.g. 106:1,113:-2 ).', default=None)
    parser.add_argument('--size', help='Font size in pixels.', type=int, default=16)
    args = parser.parse_args()

    print(args.sourceFontPathname)
    font = ImageFont.truetype(args.sourceFontPathname, args.size)

    char_array = []
    char_ranges = args.chars.split(',')
    for char_range in char_ranges:
        bounds = char_range.split('-')
        min_code = max_code = int(bounds[0])
        if len(bounds) > 1:
            max_code = int(bounds[1])
        for code in range(min_code, max_code + 1):
           char_array.append(code)

    char_array = list(set(char_array))

    char_xoffsets = [0] * len(char_array)
    if args.xoffsets:
        xoffsets = args.xoffsets.split(',')
        for xoffset in xoffsets:
            char_offset = xoffset.split(':')
            if len(char_offset) != 2:
                sys.exit(f'Unknown xoffset argument {char_offset}')
            code = int(char_offset[0])
            offset = int(char_offset[1])
            char_xoffsets[char_array.index(code)] = offset


    char_defns =  []
    char_tops = []  # Keep track of the top bounding box for each character. This is needed when shifting characters up.
    minMinTop = 0   # The minimum top value that characters must be shifted up to avoid clipping the bottom of descending characters (e.g. g, y, j, etc)
    minTop = args.size
    maxWidth = 0
    maxHeight = 0
    anchor = 'la'
    for index, code in enumerate(char_array):
        c = chr(code)
        aLeft, aTop, aRight, aBottom = font.getbbox(c, anchor=anchor)
        minTop = min(aTop, minTop)
        minMinTop = max(aBottom - args.size, minMinTop)
        height = aBottom - aTop + 1
        width = aRight
        maxWidth = max(width, maxWidth)
        maxHeight = max(height, maxHeight)
        char_tops.append(aTop)
        char_defns.append({ "Code" : f"{c}", "Width" : width, "Height" : aBottom, "Filename" : f'U{code:03d}.bmp' })
        if args.verbose:
            print(f'U{code} {c}: Left={aLeft}, Right={aRight}, Top={aTop}, Bottom={aBottom}, width={width}, height={height}')
    
    # Ensure characters are shifted up enough to avoid clipping the bottom of descending characters (e.g. g, y, j, etc)
    minTop = max(minMinTop, minTop)

    if args.verbose:
        print(f'minTop={minTop}, maxWidth={maxWidth}, maxHeight={maxHeight}')


    # Adjust the height of each character by subtracking minTop, as this is the amount the entire
    # font will be shifted up when being rendered.
    for index, _ in enumerate(char_array):
        char_defns[index]["Height"] -= minTop

    destFolder = os.path.dirname(args.fontPathname)
    ensure_folder_exists(destFolder)

    packed_font_filename = os.path.basename(args.fontPathname)
    packed_font_filename, _ = os.path.splitext(packed_font_filename)
    packed_font = {    
        "Name" : f"{packed_font_filename}.pf",
        "Height" : maxHeight,
        "Width" : rounded_width(maxWidth),
        "DefaultCharacter" : ".",
        "Characters" : char_defns
    }

    for index, code in enumerate(char_array):
        c = chr(code)
        with Image.new("1", (rounded_width(maxWidth), maxHeight)) as im:
            d = ImageDraw.Draw(im)
            # Don't shift characters up more than their top value. This avoids clipping the top of superscripts when shifting up
            # but will change their y start position in the packed font.
            y_shift_up = min(minTop, char_tops[index])
            d.text((char_xoffsets[index], -y_shift_up), f'{c}', fill="white", anchor=anchor, font=font)
            im.save(os.path.join(destFolder, f'U{code:03d}.bmp'))

    with open(args.fontPathname, 'w') as f:
       json.dump(packed_font, f, indent=4)

    print(f'Font {packed_font_filename} successfully saved to {destFolder}.')