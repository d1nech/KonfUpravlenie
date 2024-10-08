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
    
    dependencies = []
    depends_section = soup.find('summary', string=lambda text: text and 'Depends' in text)
    
    if depends_section:
        ul = depends_section.find_next('ul')
        if ul:
            for li in ul.find_all('li'):
                dep = li.text.strip()
                if dep.startswith("so:"):
                    dep = dep[3:]
                    dep = dep.split('.')[0]
                
                if dep and dep not in dependencies:
                    dependencies.append(dep)

    return dependencies

def create_dependency_graph(package_name, output_file, visited=None):
    if visited is None:
        visited = set()

    dependencies = get_dependencies(package_name)
    
    graph_lines = []
    
    for dep in dependencies:
        if dep not in visited:
            visited.add(dep)
            graph_lines.append(f"{package_name} -> {dep}")
            
            sub_dependencies = get_dependencies(dep)
            for sub_dep in sub_dependencies:
                graph_lines.append(f"{dep} -> {sub_dep}")
                create_dependency_graph(sub_dep, output_file, visited)

    with open(f"{output_file}.txt", 'w') as f:
        f.write('digraph depends{\n')
        for line in graph_lines:
            f.write(line + '\n')
        f.write('}')
    print(f"Граф зависимостей сохранен в {output_file}.txt")

def main():
    parser = argparse.ArgumentParser(description='Получить зависимости пакета из Alpine Linux.')
    parser.add_argument('--package', required=True, help='Название пакета')
    parser.add_argument('--output-file', required=True, help='Имя выходного файла для графа зависимостей (без расширения)')
    
    args = parser.parse_args()
    
    create_dependency_graph(args.package, args.output_file)

if __name__ == "__main__":
    main()
