#!/usr/bin/env python3
import sys
import json

def toNumber(no_str):
    if no_str.startswith("#"):
        return int(no_str[1:])
    return int(no_str)

def preprocessLine(line, full_mapper, screen_height, screen_width, inside=False):
    #find if there is preprocessing to be done
    dol_loc = line.find("$") if not inside else 0
    if dol_loc < 0:
        return line

    dol2_loc = line[dol_loc+1:].find("$") if not inside else len(line)
    if dol2_loc < 0:
        raise ValueError("second dollar sign not found")
    dol2_loc += dol_loc+1


    token = line[dol_loc+1:dol2_loc] if not inside else line

    subst_value = None
    if token.startswith("position("):
        comma_location = token.find(',')
        closepar_location = token.find(')')

        width = token[len("position("):comma_location]
        if not(width.isnumeric() or width[1:].isnumeric()):
            width = preprocessLine(width, full_mapper, screen_height, screen_width, True)

        height = token[comma_location+1: closepar_location]
        if not(height.isnumeric() or height[1:].isnumeric()):
            height = preprocessLine(height, full_mapper, screen_height, screen_width, True)

        width = toNumber(width)
        height = toNumber(height)

        if width > screen_width or height > screen_height:
            raise ValueError("width or height extend beyond screen")

        subst_value = f'#{width+height*screen_width}'

    elif token.startswith("sum("):
        comma_location = token.find(',')
        closepar_location = token.find(')')

        x = token[len("sum("):comma_location]
        if not(x.isnumeric() or x[1:].isnumeric()):
            x = preprocessLine(x, full_mapper, screen_height, screen_width, True)

        y = token[comma_location+1: closepar_location]
        if not(y.isnumeric() or y[1:].isnumeric()):
            y = preprocessLine(y, full_mapper, screen_height, screen_width, True)

        x = toNumber(x)
        y = toNumber(y)

        subst_value = f'#{x+y}'
    else:
        subst_value = full_mapper[token]


    newline = line[:dol_loc] + subst_value + line[dol2_loc+1:]

    #use recursion if there is more than one substitution in the same line
    return preprocessLine(newline, full_mapper, screen_height, screen_width)

def createFullMapper(base_mapper, user_defs):
    start_char = mapper["start_char"]
    color_spacing = mapper["color_spacing"]
    colors = mapper["colors"]
    chars = mapper["chars"]

    color_dict = {
        color : f'#{i*color_spacing}'
        for i, color in enumerate(colors)
    }

    char_dict = {
        char : f'#{i+start_char}'
        for i, char in enumerate(chars)
    }

    combinations_dict = {
        f'{color}_{char}' : f'#{i*color_spacing+j+start_char}'
        for i, color in enumerate(colors) for j, char in enumerate(chars)
    }

    full_mapper = user_defs.copy()
    full_mapper.update(combinations_dict)
    full_mapper.update(color_dict)
    full_mapper.update(char_dict)
    return full_mapper


def preprocess(base_mapper, user_defs, file_in, file_out):
    full_mapper = createFullMapper(base_mapper, user_defs)
    screen_height = base_mapper["screen_height"]
    screen_width = base_mapper["screen_width"]

    lineno = 1
    try:
        for line in file_in:
            newline = preprocessLine(
                    line, full_mapper, screen_height, screen_width
            )
            file_out.write(newline)

            lineno += 1
    except (ValueError, KeyError) as e:
        print(f"error at line {lineno}: {e}", file=sys.stderr)
        sys.exit(-1)


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print(
            f"usage: {sys.argv[0]} charmap.json user_defs.json"
            f"file_in.asm file_out.asm", file=sys.stderr
        )
        sys.exit(-1)

    file_mapper = open(sys.argv[1], "r")
    mapper = json.load(file_mapper)
    file_mapper.close()

    file_user_defs = open(sys.argv[2], "r")
    user_defs = json.load(file_user_defs)
    file_user_defs.close()

    file_in = open(sys.argv[3], "r")
    file_out = open(sys.argv[4], "w")

    preprocess(mapper, user_defs, file_in, file_out)

    file_in.close()
    file_out.close()
