import re
import json
from typing import Any, Dict, List, Union

def parse_value(value: str) -> Union[int, List[Any], Dict[str, Any]]:
    value = value.strip()
    
    # Обработка массивов
    if value.startswith('(') and value.endswith(')'):
        value = value[1:-1].strip()
        elements = [parse_value(el.strip()) for el in value.split(',')] if value else []
        return elements
    
    # Обработка словарей
    if value.startswith('dict(') and value.endswith(')'):
        value = value[5:-1].strip()
        items = [item.strip() for item in value.split(',')]
        dct = {}
        for item in items:
            key_value = item.split('=')
            if len(key_value) != 2:
                raise ValueError(f"Invalid dictionary entry: {item}")
            key = key_value[0].strip()
            val = parse_value(key_value[1].strip())
            dct[key] = val
        return dct

    # Обработка чисел
    if re.match(r'^\d+$', value):
        return int(value)

    raise ValueError(f"Invalid value: {value}")

def parse_assignment(line: str) -> (str, Any):
    if not line.endswith(';'):
        raise ValueError("Line must end with a semicolon.")
    
    line = line[:-1].strip()
    match = re.match(r'def\s+([_a-zA-Z]+)\s*=\s*(.+)', line)
    if match:
        name = match.group(1).strip()
        value = parse_value(match.group(2).strip())
        return name, value

    match = re.match(r'\$(.+?)\$', line)
    if match:
        expression = match.group(1).strip()
        return expression, None  # Позиция для обработки выражения
    
    raise ValueError(f"Invalid assignment: {line}")

def main():
    all_data = {}
    root = all_data
    
    while True:
        try:
            line = input()
            if line.strip() == 'stop':
                break
            
            if line.startswith('--[[') and line.endswith(']]'):
                continue  # Игнорируем многострочные комментарии
            
            if line.startswith('def'):
                key, var = parse_assignment(line)
                all_data[key] = var
            
            elif line.startswith('(') or line.startswith('dict('):
                key, var = parse_assignment(line)
                all_data[key] = var
            
            else:
                match = re.match(r'\[([_a-zA-Z]+)\]', line)
                if match:
                    name = match.group(1)
                    if name in all_data:
                        print(all_data[name])
                    else:
                        print("error not in memory")
            
        except ValueError as e:
            print(e)

    print(json.dumps(all_data, indent=4))

if __name__ == '__main__':
    main()
