import argparse
import requests
from bs4 import BeautifulSoup
import graphviz

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
        dep_list = soup.find_all('a', class_='pure-menu-link')  # Замените на актуальный селектор
        for dep in dep_list:
            dependencies.add(dep.text.strip())
            
    except requests.RequestException as e:
        print(f"Ошибка при получении зависимостей для {package_name}: {e}")
    return dependencies

def create_dependency_graph(dependencies, package_name, output_file):
    """Создает граф зависимостей и сохраняет его в текстовом формате DOT."""
    with open(output_file, 'w') as f:
        f.write('digraph G {\n')
        f.write(f'    "{package_name}"\n')
        
        for dep in dependencies:
            f.write(f'    "{dep}"\n')
            f.write(f'    "{package_name}" -> "{dep}";\n')  # Создаем стрелку от пакета к зависимости
        
        f.write('}\n')
    
    print(f"Граф зависимостей сохранен в {output_file}.")

def main():
    parser = argparse.ArgumentParser(description='Получение зависимостей для пакетов Alpine Linux.')
    parser.add_argument('--package', required=True, help='Имя пакета для получения зависимостей')
    parser.add_argument('--output-file', required=True, help='Имя выходного файла (с расширением .txt)')
    parser.add_argument('--output-path', default='./', help='Путь для сохранения файла (по умолчанию ./)')

    args = parser.parse_args()

    # Формируем полный путь для сохранения
    full_output_path = f"{args.output_path}/{args.output_file}"

    # Получаем зависимости
    dependencies = get_dependencies(args.package)

    # Создаем граф зависимостей и сохраняем его в текстовом формате DOT
    create_dependency_graph(dependencies, args.package, full_output_path)

if __name__ == "__main__":
    main()
