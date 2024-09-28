import argparse
import subprocess
import os
from graphviz import Digraph

def get_dependencies(package_path):
    """Получает зависимости пакета из файла APK."""
    dependencies = set()
    try:
        with open(package_path, 'r') as f:
            for line in f:
                if line.startswith("depends:"):
                    deps = line.split(":")[1].strip().split()
                    dependencies.update(deps)
    except Exception as e:
        print(f"Ошибка при чтении файла: {e}")
    return dependencies

def build_graph(dependencies):
    """Строит граф зависимостей с помощью Graphviz."""
    dot = Digraph(comment='Граф зависимостей')
    
    for dep in dependencies:
        dot.node(dep)  

    for dep in dependencies:
        dot.edge(dep, dep)  
    
    return dot

def save_graph_to_file(dot, output_file):
    """Сохраняет граф в файл."""
    try:
        dot.render(output_file, format='png', cleanup=True)  # Сохранение в формате PNG
        print(f"Граф сохранен в {output_file}.png")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

def main():
    parser = argparse.ArgumentParser(description='Визуализатор графа зависимостей для пакетов Alpine Linux.')
    parser.add_argument('package_path', help='Путь к анализируемому пакету.')
    parser.add_argument('output_path', help='Имя выходного файла (без расширения).')

    args = parser.parse_args()

    # Получаем зависимости
    dependencies = get_dependencies(args.package_path)

    # Строим граф
    dot = build_graph(dependencies)

    # Сохраняем граф в файл
    save_graph_to_file(dot, args.output_path)

if __name__ == "__main__":
    main()

