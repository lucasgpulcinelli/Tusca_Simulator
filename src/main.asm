
msg: string "Hello, World!"

main:
    loadn r0, $starting_pos$
    loadn r1, #msg
    loadn r2, #0

print_loop:
    loadi r3, r1
    outchar r3, r0
    inc r0
    inc r1
    cmp r3, r2
    jne print_loop

    halt
