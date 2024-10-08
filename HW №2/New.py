import argparse
import requests
from bs4 import BeautifulSoup
from graphviz import Digraph

def get_dependencies(package_name):
    """Получает зависимости пакета из Alpine Linux через HTTP-запрос."""
    dependencies = set()
    url = f"https://pkgs.alpinelinux.org/package/v3.15/main/x86_64/{package_name}"  # Замените на актуальную версию и архитектуру

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверка на ошибки HTTP
        soup = BeautifulSoup(response.text, 'html.parser')

        # Предположим, что зависимости находятся в определенном элементе
        # Это нужно адаптировать под структуру страницы
        dep_list = soup.find_all('li', class_='dependency')  # Замените на актуальный селектор
        for dep in dep_list:
            dependencies.add(dep.text.strip())
            
    except requests.RequestException as e:
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
    parser.add_argument('--package', required=True, help='Имя пакета для получения зависимостей')
    parser.add_argument('--output-file', required=True, help='Имя выходного файла (без расширения)')
    parser.add_argument('--output-path', default='./', help='Путь для сохранения файла (по умолчанию ./)')

    args = parser.parse_args()

    # Формируем полный путь для сохранения
    full_output_path = f"{args.output_path}/{args.output_file}"

    # Получаем зависимости
    dependencies = get_dependencies(args.package)

    # Строим граф
    graph = build_graph(dependencies)

    # Сохраняем граф в файл
    save_graph_to_file(graph, full_output_path)

    # Сохраняем зависимости в текстовый файл
    save_dependencies_to_txt(dependencies, f"{full_output_path}.txt")

if __name__ == "__main__":
    main()
