; simple file describing the preprocessor capabilites

msg: var $MSGLEN$; simple user defined substitutions to numbers work (see user_defs.json)
static msg + #0, $green_h$; characters can be in the format 'color_char' (all chars are in res/charmap/charmap.json)
static msg + #1, $red_e$
static msg + #2, $purple_x$
static msg + #3, $black_space$
static msg + #4, $poolgreen_f$
static msg + #5, $poolgreen_f$
static msg + #6, $greaterthan$; characters without color default to white
static msg + #7, $white_a$
static msg + #8, $grey_l$
static msg + #9, $cyan_l$
static msg + #10, $green$; and colors default to the character #0 for this color


main:
    loadn r0, $starting_pos$; definitions can have other definitions inside them, see user_defs.json
    loadn r1, #msg
    loadn r2, $sum(starting_pos,MSGLEN)$; 'macros' can be used with definitions or constant numbers

print_loop:
    loadi r3, r1
    outchar r3, r0
    inc r0
    inc r1
    cmp r0, r2
    jne print_loop

    halt
