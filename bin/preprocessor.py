#!/usr/bin/env python3
import sys
import json
import re

def toNumber(no_str):
    '''
    toNumber transforms a number to a string (both if the number can be
    directly converted or if the number has a leading #)
    '''
    if no_str.startswith("#"):
        return int(no_str[1:])
    return int(no_str)

def preprocessLine(line, defs_mapper, macro_mapper, inside=False):
    '''
    preprocessLine does all the substitutions for a single line, using a
    definitions and macro mapper, besides a flag for if the call was made
    from inside a 'macro' call.

    All tokens that should be substituted need to be in the format
    $text_to_substitute or $macro(argument_1,argument_2,[...]).
    Note that macro calls cannot have any spaces, same as definitions
    '''
    
    #matches any token that needs preprocessing
    match_any = re.search(f"\${'?' if inside else ''}([\w\(,\))]+)", line)
    if not match_any:
        return line
    
    start, end = match_any.span()

    #actual thing that needs preprocessing, without leading '$'
    token = match_any.group(1)

    #matches a 'macro'
    match_macro = re.match("(\w+)\(([\w,]+)\)", token)
    if not match_macro:
        new_line = line[:start] + defs_mapper[token] + line[end:]
        return new_line

    macro_str = match_macro.group(1)
    arguments_str = match_macro.group(2).split(sep=",")

    macro = macro_mapper[macro_str]
    
    arg = []
    for arg_str in arguments_str:
        #if the argument is a definition or another macro call:
        if not re.match("#?\d+", arg_str):
            arg_str = preprocessLine(arg_str, defs_mapper, macro_mapper, 
                True
            )
        
        arg.append(toNumber(arg_str))

    macro_globals = {
        "arg":arg, 
        "sw":defs_mapper["screen_width"], 
        "sh":defs_mapper["screen_height"],
        "defs":defs_mapper
    }

    new_line = line[:start] + f'#{eval(macro, macro_globals)}' + line[end:]
    return new_line

def createDefs(line, defs_mapper, macro_mapper):
    '''
    createDefs creates macros and definitions based on the 
    (already preprocessed) line. The definitions must be in the format
    "#define name value" for definitions, and "#define macro() expression"
    for macros. 
    
    The macro is written in python and has some variables: arg is an array with
    all arguments, sw and sh are the screen width and height in pixels, and
    defs is a dict with all definitions.
    '''

    match = re.match("#define (\w+) ([\w#]+)", line)
    if match:
        def_name = match.group(1)
        def_value = match.group(2)

        defs_mapper[def_name] = def_value
        return True
    
    match = re.match("#define (\w+)\(\) ([\w+*/%\[\]\(\) #]+)", line)
    if not match:
        return False
    
    func_name = match.group(1)
    func_def = match.group(2).replace("#","")

    macro_mapper[func_name] = func_def
    
    return True


def createFullMappers(base_mapper):
    '''
    createFullMapper creates the actual mappers from the json stored.
    The whole mapper is a simple dictionary with the text to be substituted.

    The macros mapper has two basic functions: sum and position. The latter
    just returns the screen position of the pixel at a certain width and height
    '''
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

    full_mapper = {}
    full_mapper["screen_height"] = base_mapper["screen_height"]
    full_mapper["screen_width"] = base_mapper["screen_width"]
    full_mapper.update(combinations_dict)
    full_mapper.update(color_dict)
    full_mapper.update(char_dict)
    return full_mapper, {"sum": "arg[0]+arg[1]", "position":"arg[0]+arg[1]*sw"}

def preprocess(base_mapper, file_in, file_out):
    '''
    preprocess does the full preprocessing in the file using a base mapper
    '''
    defs_mapper, macro_mapper = createFullMappers(base_mapper)

    lineno = 1
    for line in file_in:
        newline = preprocessLine(line, defs_mapper, macro_mapper)
        created = createDefs(newline, defs_mapper, macro_mapper)
        if not created:
            file_out.write(newline)

        lineno += 1



if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(
            f"usage: {sys.argv[0]} charmap.json "
            f"file_in.asm file_out.asm", file=sys.stderr
        )
        sys.exit(-1)

    file_mapper = open(sys.argv[1], "r")
    mapper = json.load(file_mapper)
    file_mapper.close()

    file_in = open(sys.argv[2], "r")
    file_out = open(sys.argv[3], "w")

    preprocess(mapper, file_in, file_out)

    file_in.close()
    file_out.close()
