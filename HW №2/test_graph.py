import pytest
from main import get_dependencies, build_graph, save_graph_to_file
from graphviz import Digraph
import os

# Тестируем функцию получения зависимостей
def test_get_dependencies(tmp_path):
    # Создаем временный файл с зависимостями
    test_file = tmp_path / "test_package.txt"
    test_file.write_text("depends: package1 package2\n")

    dependencies = get_dependencies(test_file)

    assert dependencies == {"package1", "package2"}

def test_get_dependencies_empty_file(tmp_path):
    # Создаем пустой файл
    test_file = tmp_path / "empty_package.txt"
    test_file.write_text("")

    dependencies = get_dependencies(test_file)

    assert dependencies == set()

def test_get_dependencies_invalid_file(tmp_path):
    # Создаем файл с неправильным форматом
    test_file = tmp_path / "invalid_package.txt"
    test_file.write_text("some random text\n")

    dependencies = get_dependencies(test_file)

    assert dependencies == set()

# Тестируем функцию построения графа
def test_build_graph():
    dependencies = {"package1", "package2"}
    dot = build_graph(dependencies)

    assert isinstance(dot, Digraph)
    assert len(dot.body) == 4  # Должно быть два узла

# Тестируем сохранение графа (можно проверить только, что функция выполняется)
def test_save_graph_to_file(tmp_path):
    dot = Digraph(comment='Test Graph')
    dot.node('A')
    dot.node('B')
    
    output_file = tmp_path / "test_output"
    
    save_graph_to_file(dot, output_file)

    # Проверяем, что файл был создан
    assert os.path.exists(f"{output_file}.png")

# Запуск тестов
if __name__ == "__main__":
    pytest.main()
