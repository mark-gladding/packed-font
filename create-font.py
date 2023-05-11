import argparse
import json
from PIL import Image, ImageFont, ImageDraw
import os

def len_in_bytes(pixels):
    return int((pixels + 7) / 8)

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
    parser.add_argument('--firstChar', help='Character code of first character to create.', type=int, default=32)
    parser.add_argument('--lastChar', help='Character code of last character to create.', type=int, default=127)
    parser.add_argument('--size', help='Font size in pixels.', default=16)
    args = parser.parse_args()

    print(args.sourceFontPathname)
    font = ImageFont.truetype(args.sourceFontPathname, args.size)

    char_defns =  []
    minTop = args.size
    maxWidth = 0
    maxHeight = 0
    for code in range(args.firstChar, args.lastChar + 1):
        c = chr(code)
        aLeft, aTop, aRight, aBottom = font.getbbox(c)
        minTop = min(aTop, minTop)
        height = aBottom - aTop + 1
        width = aRight
        maxWidth = max(width, maxWidth)
        maxHeight = max(height, maxHeight)
        char_defns.append({ "Code" : f"{c}", "Width" : width, "Height" : aBottom, "Filename" : f'U{code:03d}.bmp' })
        if args.verbose:
            print(f'{c}: Left={aLeft}, Right={aRight}, Top={aTop}, Bottom={aBottom}, width={width}, height={height}')
    
    if args.verbose:
        print(f'minTop={minTop}, maxWidth={maxWidth}, maxHeight={maxHeight}')

    # Adjust the height of each character by subtracking minTop, as this is the amount the entire
    # font will be shifted up when being rendered.
    for code in range(args.firstChar, args.lastChar + 1):
        char_defns[code - args.firstChar]["Height"] -= minTop

    destFolder = os.path.dirname(args.fontPathname)
    ensure_folder_exists(destFolder)

    packed_font_filename = os.path.basename(args.fontPathname)
    packed_font_filename, _ = os.path.splitext(packed_font_filename)
    packed_font = {    
        "Name" : f"{packed_font_filename}.pf",
        "Height" : maxHeight,
        "Width" : maxWidth,
        "DefaultCharacter" : ".",
        "Characters" : char_defns
    }

    for code in range(args.firstChar, args.lastChar + 1):
        c = chr(code)
        with Image.new("1", (maxWidth, maxHeight)) as im:
            d = ImageDraw.Draw(im)
            d.text((0, -minTop), f'{c}', fill="white", anchor="la", font=font)
            im.save(os.path.join(destFolder, f'U{code:03d}.bmp'))

    with open(args.fontPathname, 'w') as f:
       json.dump(packed_font, f, indent=4)

    print(f'Font {packed_font_filename} successfully saved to {destFolder}.')