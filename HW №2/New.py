import requests
from bs4 import BeautifulSoup
import argparse
import graphviz

def get_dependencies(package_name):
    url = f"https://pkgs.alpinelinux.org/package/v3.14/main/x86_64/{package_name}"
    response = requests.get(url)
    
    if response.status_code != 200:
        print(f"Ошибка при получении данных для пакета {package_name}: {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Ищем блок с зависимостями
    dependencies = []
    depends_section = soup.find('summary', string=lambda text: text and 'Depends' in text)
    
    if depends_section:
        # Находим следующий элемент списка после "Depends"
        ul = depends_section.find_next('ul')
        if ul:
            for li in ul.find_all('li'):
                dep = li.text.strip()
                if dep and dep not in dependencies:
                    dependencies.append(dep)

    return dependencies

def create_dependency_graph(package_name, output_file):
    dependencies = get_dependencies(package_name)
    
    with open(output_file, 'w') as f:
        f.write("digraph dependencies {\n")
        for dep in dependencies:
            f.write(f'    "{package_name}" -> "{dep}";\n')
        f.write("}\n")
    
    print(f"Граф зависимостей сохранен в {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Получить зависимости пакета из Alpine Linux.')
    parser.add_argument('--package', required=True, help='Название пакета')
    parser.add_argument('--output-file', required=True, help='Имя выходного файла для графа зависимостей')
    
    args = parser.parse_args()
    
    create_dependency_graph(args.package, args.output_file)

if __name__ == "__main__":
    main()
