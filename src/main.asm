
msg: var $MSGLEN$
static msg + #0, $green_h$
static msg + #1, $red_e$
static msg + #2, $purple_x$
static msg + #3, $black_space$
static msg + #4, $poolgreen_f$
static msg + #5, $poolgreen_f$
static msg + #6, $greaterthan$
static msg + #7, $white_a$
static msg + #8, $grey_l$
static msg + #9, $cyan_l$
static msg + #10, $green$


main:
    loadn r0, $starting_pos$
    loadn r1, #msg
    loadn r2, $sum(starting_pos,MSGLEN)$

print_loop:
    loadi r3, r1
    outchar r3, r0
    inc r0
    inc r1
    cmp r0, r2
    jne print_loop

    halt
