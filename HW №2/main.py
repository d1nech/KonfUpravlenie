import argparse
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
    """Строит граф зависимостей с использованием библиотеки Graphviz."""
    dot = Digraph(comment='Dependency Graph')

    # Добавляем узлы и связи
    for dep in dependencies:
        dot.node(dep)  # Добавляем узел для каждой зависимости
        # Пример связи с самим собой (можно изменить по необходимости)
        dot.edge(dep, dep)  

    return dot

def save_graph_to_file(graph, output_file):
    """Сохраняет граф в файл формата DOT или изображение."""
    try:
        graph.render(output_file, format='png', cleanup=True)  # Сохраняем в PNG
        print(f"Граф сохранен в {output_file}.png")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

def save_dependencies_to_txt(dependencies, output_file):
    """Сохраняет зависимости в текстовый файл в формате a -> b."""
    try:
        with open(output_file, 'w') as f:
            for dep in dependencies:
                f.write(f"{dep} -> {dep}\n")  # Пример связи с самим собой
        print(f"Зависимости сохранены в {output_file}")
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
    graph = build_graph(dependencies)

    # Сохраняем граф в файл
    save_graph_to_file(graph, args.output_path)

    # Сохраняем зависимости в текстовый файл
    save_dependencies_to_txt(dependencies, f"{args.output_path}.txt")

if __name__ == "__main__":
    main()
