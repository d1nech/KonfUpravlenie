def assembler(code):
    bc = []
    for op, *args in code:
        if op == 'move':
            b, c = args
            bc += serializer(17, ((b, 5), (c, 15)), 3)
        if op == 'read':
            b, c, d = args
            bc += serializer(3, ((b, 5), (c, 12), (d, 26)), 5)
        if op == 'write':
            b, c, d = args
            bc += serializer(1, ((b, 5), (c, 12), (d, 19)), 5)
        if op == 'bitwise_rotate_right':
            b, c = args
            bc += serializer(21, ((b, 5), (c, 34)), 6)
    return bc

def serializer(cmd, fields, size):
    bits = 0
    bits |= cmd
    for value, offset in fields:
        bits |= (value << offset)
    return bits.to_bytes(size, 'little')
