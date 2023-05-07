
import sys

def len_in_bytes(pixels):
    return int(pixels / 8)

with open('digits.pf', 'rb') as f:
    data = f.read()

print(f'Font file size = {len(data)}')

if len(data) < 6 or data[0] != ord('P') or data[1] != ord('F'):
    print('Unknown file format')
    sys.exit(-1)

width = data[2]
height = data[3]
width_in_bytes = data[4] + data[5] * 256
character_count = data[6]

print(f'Reading font size {width}x{height}, width in bytes {width_in_bytes} with {character_count} characters.')

index = 7

for i in range(character_count):
    character = chr(data[index])
    print(character)
    index += 1
    char_width = data[index]
    index += 1
    yoffset = data[index]
    index += 1
    start_index = data[index] + data[index + 1] * 256
    index += 2

for i in range(character_count):
    for j in range(height):
        row = []
        for b in range(len_in_bytes(char_width)):
            val = data[index]
            for k in range(8):
                row.append((val >> (7 - k)) & 1)
            index += 1
        print(row)
    print()

    #       Character code (1 byte)
    #       Width (1 byte)
    #       YOffset (1 byte)
    #       StartIndex (2 bytes)
    #       Character data