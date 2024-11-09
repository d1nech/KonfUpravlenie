import re
import json
from typing import Any, Dict, List

def parse_value(value: str, memory: Dict[str, Any]) -> Any:
    value = value.strip()

    # Array parsing with support for nested arrays
    if value.startswith('({') and value.endswith('})'):
        value = value[2:-2].strip()
        elements = []
        current_element = ""
        nesting_level = 0

        for i, char in enumerate(value):
            if char == '(' and i + 1 < len(value) and value[i + 1] == '{':
                nesting_level += 1
                current_element += char
            elif char == '}' and nesting_level > 0:
                nesting_level -= 1
                current_element += char
            elif char == ',' and nesting_level == 0:
                elements.append(parse_value(current_element.strip(), memory))
                current_element = ""
            else:
                current_element += char

        if current_element:
            elements.append(parse_value(current_element.strip(), memory))
        return elements

    # Dictionary parsing with recursion for nested dictionaries
    if value.startswith('dict(') and value.endswith(')'):
        value = value[5:-1].strip()
        items = re.split(r',\s*(?=\w+\s*=)', value)
        dct = {}
        for item in items:
            key_value = item.split('=', 1)
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

    # Boolean parsing
    if value in {"True", "False"}:
        return value == "True"

    # Variable lookup
    if value in memory:
        return memory[value]

    raise ValueError(f"Invalid value: {value}")

def parse_assignment(line: str, memory: Dict[str, Any]) -> (str, Any):
    line = line.strip()  # Remove surrounding whitespace

    match = re.match(r'def\s+([_a-zA-Z]+)\s*=\s*(.+)', line)
    if match:
        name = match.group(1).strip()
        value = match.group(2).strip()

        # Check if the value is a dictionary or array
        if (value.startswith('({') and value.endswith('})')) or (value.startswith('dict(') and value.endswith(')')):
            value = parse_value(value, memory)
        elif not (value.startswith('({') or value.startswith('dict(')):
            value = parse_value(value, memory)

        return name, value

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
