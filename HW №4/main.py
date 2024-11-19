import argparse
import xml.etree.ElementTree as ET

def assembler(input_file, output_file, log_file):
    with open(input_file, 'r') as f:
        code = [eval(line.strip()) for line in f.readlines()]
    
    bc = []
    log_entries = []
    for line_num, (op, *args) in enumerate(code, start=1):
        try:
            if op == 'move':
                if len(args) != 2:
                    raise ValueError(f"Line {line_num}: Expected 2 arguments for 'move', got {len(args)}")
                b, c = args
                bc += serializer(17, ((b, 5), (c, 15)), 3)
                log_entries.append(f"move b={b} c={c}")
            elif op == 'read':
                if len(args) != 3:
                    raise ValueError(f"Line {line_num}: Expected 3 arguments for 'read', got {len(args)}")
                b, c, d = args
                bc += serializer(3, ((b, 5), (c, 12), (d, 26)), 5)
                log_entries.append(f"read b={b} c={c} d={d}")
            elif op == 'write':
                if len(args) != 3:
                    raise ValueError(f"Line {line_num}: Expected 3 arguments for 'write', got {len(args)}")
                b, c, d = args
                bc += serializer(1, ((b, 5), (c, 12), (d, 19)), 5)
                log_entries.append(f"write b={b} c={c} d={d}")
            elif op == 'bitwise_rotate_right':
                if len(args) != 2:
                    raise ValueError(f"Line {line_num}: Expected 2 arguments for 'bitwise_rotate_right', got {len(args)}")
                b, c = args
                bc += serializer(21, ((b, 5), (c, 34)), 6)
                log_entries.append(f"bitwise_rotate_right b={b} c={c}")
            else:
                raise ValueError(f"Line {line_num}: Unknown operation '{op}'")
        except ValueError as e:
            print(f"Error in input file: {e}")
            return
    
    # Write binary output
    with open(output_file, 'wb') as f:
        f.write(bytearray(bc))
    
    # Write log file
    root = ET.Element("log")
    for entry in log_entries:
        instruction = ET.SubElement(root, "instruction")
        instruction.text = entry
    tree = ET.ElementTree(root)
    tree.write(log_file)

def serializer(cmd, fields, size):
    bits = 0
    bits |= cmd
    for value, offset in fields:
        bits |= (value << offset)
    return bits.to_bytes(size, 'little')

def interpreter(input_file, output_file, mem_range):
    with open(input_file, 'rb') as f:
        bc = f.read()
    
    memory = [0] * 100  # Увеличили размер памяти, чтобы избежать ошибок
    regs = [0] * 10     # Увеличили количество регистров для безопасности
    
    # Deserialize and execute commands from binary code
    # Here we assume a specific parsing logic for commands
    cmds = parse_binary_commands(bc)
    for op, *args in cmds:
        if op == "move":
            address, const = args
            regs[address] = const
        elif op == "write":
            target, source = args
            memory[regs[target]] = regs[source]
        elif op == "read":
            target, addr, dest = args
            regs[dest] = memory[regs[addr]]
        elif op == "bitwise_rotate_right":
            dest, src, num_bits = args
            regs[dest] = (regs[src] >> num_bits) | (regs[src] << (32 - num_bits) & 0xFFFFFFFF)
    
    # Write results to output XML file
    root = ET.Element("memory")
    for addr in range(mem_range[0], mem_range[1]):
        mem_entry = ET.SubElement(root, "address", attrib={"index": str(addr)})
        mem_entry.text = str(memory[addr])
    tree = ET.ElementTree(root)
    tree.write(output_file)

def parse_binary_commands(bc):

    return []

def main():
    parser = argparse.ArgumentParser(description='Assembler and Interpreter for a custom VM.')
    subparsers = parser.add_subparsers(dest='command')

    # Assembler arguments
    asm_parser = subparsers.add_parser('assemble', help='Assemble source code into binary')
    asm_parser.add_argument('input_file', help='Path to the input source file')
    asm_parser.add_argument('output_file', help='Path to the output binary file')
    asm_parser.add_argument('log_file', help='Path to the log XML file')

    # Interpreter arguments
    int_parser = subparsers.add_parser('interpret', help='Interpret binary file')
    int_parser.add_argument('input_file', help='Path to the input binary file')
    int_parser.add_argument('output_file', help='Path to the output XML file')
    int_parser.add_argument('mem_range', type=int, nargs=2, help='Range of memory to output (start end)')

    args = parser.parse_args()
    if args.command == 'assemble':
        assembler(args.input_file, args.output_file, args.log_file)
    elif args.command == 'interpret':
        interpreter(args.input_file, args.output_file, args.mem_range)

if __name__ == "__main__":
    main()
