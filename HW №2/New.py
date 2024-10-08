import argparse
import subprocess
from graphviz import Digraph

def get_dependencies(package_name):
    """Получает зависимости пакета из Alpine Linux с помощью apk."""
    dependencies = set()
    try:
        # Запускаем команду apk для получения зависимостей
        result = subprocess.run(['apk', 'info', '--depends', package_name], 
                                capture_output=True, text=True, check=True)
        
        # Обрабатываем вывод
        for line in result.stdout.splitlines():
            dep = line.strip()
            if dep:
                dependencies.add(dep)
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при получении зависимостей для {package_name}: {e}")
    return dependencies

def build_graph(dependencies):
    """Строит граф зависимостей с использованием библиотеки Graphviz."""
    dot = Digraph(comment='Dependency Graph')

    # Добавляем узлы и связи
    for dep in dependencies:
        dot.node(dep)  # Добавляем узел для каждой зависимости

    return dot

def save_graph_to_file(graph, output_file):
    """Сохраняет граф в файл формата DOT или изображение."""
    try:
        graph.render(output_file, format='png', cleanup=True)  # Сохраняем в PNG
        print(f"Граф сохранен в {output_file}.png")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

def save_dependencies_to_txt(dependencies, output_file):
    """Сохраняет зависимости в текстовый файл."""
    try:
        with open(output_file, 'w') as f:
            for dep in dependencies:
                f.write(f"{dep}\n")  # Печатаем только зависимости
        print(f"Зависимости сохранены в {output_file}")
    except Exception as e:
        print(f"Ошибка при записи в файл: {e}")

def main():
    parser = argparse.ArgumentParser(description='Визуализатор графа зависимостей для пакетов Alpine Linux.')
    
    # Получаем имя пакета от пользователя
    package_name = input("Введите имя пакета: ")
    
    # Получаем имя выходного файла от пользователя
    output_file_name = input("Введите имя выходного файла (без расширения): ")
    
    # Получаем путь для сохранения от пользователя
    output_path = input("Введите путь для сохранения файла (например, ./): ")
    
    full_output_path = f"{output_path}/{output_file_name}"

    # Получаем зависимости
    dependencies = get_dependencies(package_name)

    # Строим граф
    graph = build_graph(dependencies)

    # Сохраняем граф в файл
    save_graph_to_file(graph, full_output_path)

    # Сохраняем зависимости в текстовый файл
    save_dependencies_to_txt(dependencies, f"{full_output_path}.txt")

if __name__ == "__main__":
    main()
