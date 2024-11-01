import re
import json
from typing import Any, Dict, List, Union

def parse_value(value: str, memory: Dict[str, Any]) -> Any:
    value = value.strip()

    # Array parsing
    if value.startswith('({') and value.endswith('})'):
        value = value[2:-2].strip()
        elements = [parse_value(el.strip(), memory) for el in value.split(',')] if value else []
        return elements

    # Dictionary parsing
    if value.startswith('dict(') and value.endswith(')'):
        value = value[5:-1].strip()
        items = [item.strip() for item in re.split(r',\s*(?=\w+\s*=)', value)]
        dct = {}
        for item in items:
            key_value = item.split('=')
            if len(key_value) != 2:
                raise ValueError(f"Invalid dictionary entry: {item}")
            key = key_value[0].strip()
            val = parse_value(key_value[1].strip(), memory)
            dct[key] = val
        return dct

    # String parsing
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]  # Remove quotes

    # Numeric parsing
    if re.match(r'^\d+$', value):
        return int(value)

    # Variable lookup
    if value in memory:
        return memory[value]

    # Expression evaluation
    match = re.match(r'^\$(\S+)\s+(.+?)\s*\$$', value)
    if match:
        operation = match.group(1)
        operands = match.group(2).strip().split()
        return evaluate_expression(operation, operands, memory)

    raise ValueError(f"Invalid value: {value}")

def evaluate_expression(operation: str, operands: List[str], memory: Dict[str, Any]) -> Any:
    if operation not in {'+', '-', '*', '/', 'max'}:
        raise ValueError(f"Invalid operation: {operation}")

    values = [parse_value(op.strip(), memory) for op in operands]

    if operation == '+':
        return sum(values)
    elif operation == '-':
        return values[0] - sum(values[1:])
    elif operation == '*':
        result = 1
        for v in values:
            result *= v
        return result
    elif operation == '/':
        if len(values) != 2:
            raise ValueError("Division requires exactly two operands.")
        return values[0] / values[1]
    elif operation == 'max':
        return max(values)

def parse_assignment(line: str, memory: Dict[str, Any]) -> (str, Any):
    if not line.endswith(';'):
        raise ValueError("Line must end with a semicolon.")

    line = line[:-1].strip()
    match = re.match(r'def\s+([_a-zA-Z]+)\s*=\s*(.+)', line)
    if match:
        name = match.group(1).strip()
        value = parse_value(match.group(2).strip(), memory)
        return name, value

    # Handle any array assignment
    if '=' in line:
        key, value = line.split('=', 1)
        key = key.strip()
        value = value.strip()
        if value.startswith('(') and value.endswith(')'):
            value = parse_value(value, memory)
            return key, value

        # Handle dict assignment as well
        if value.startswith('dict('):
            value = parse_value(value, memory)
            return key, value

    raise ValueError(f"Invalid assignment: {line}")

def main():
    memory = {}
    
    while True:
        try:
            line = input()
            if line.strip() == 'stop':
                break
            
            if line.startswith('--[[') and line.endswith(']]'):
                continue  # Ignore multi-line comments
            
            # All assignments are handled by parse_assignment
            key, var = parse_assignment(line, memory)
            memory[key] = var
            
        except ValueError as e:
            print(e)

    # Print all memory content in JSON format
    print(json.dumps(memory, indent=4))

if __name__ == '__main__':
    main()
