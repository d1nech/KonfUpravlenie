import pytest
import graphviz
from unittest.mock import patch, Mock
from main import get_dependencies, create_dependency_graph

# Тест для функции get_dependencies
def test_get_dependencies():
    package_name = "example-package"
    
    # Создаем фиктивный HTML-контент для ответа
    mock_html = """
    <html>
        <body>
            <summary>Depends on:</summary>
            <ul>
                <li>so:libc.so.6</li>
                <li>so:libm.so.6</li>
                <li>other-package</li>
            </ul>
        </body>
    </html>
    """
    
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = mock_html.encode('utf-8')
        mock_get.return_value = mock_response
        
        dependencies = get_dependencies(package_name)
        
        assert dependencies == ['libc', 'libm', 'other-package']

def test_get_dependencies_invalid_package():
    package_name = "invalid-package"
    
    with patch('requests.get') as mock_get:
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        dependencies = get_dependencies(package_name)
        
        assert dependencies == []

# Тест для функции create_dependency_graph
@patch('main.get_dependencies')
def test_create_dependency_graph(mock_get_dependencies):
    mock_get_dependencies.side_effect = [
        ['dep1', 'dep2'],  # Зависимости для package_name
        ['subdep1'],       # Зависимости для dep1
        []                 # Зависимости для dep2 (пусто)
    ]
    
    output_file = 'test_output'
    
    # Запускаем функцию
    create_dependency_graph('package_name', output_file)
    
    # Проверяем, что файл был создан и содержит правильные данные
    with open(f"{output_file}.txt", 'r') as f:
        content = f.read()
        
    expected_content = (
        'digraph depends{n'
        '"package_name" -> "dep1"n'
        '"package_name" -> "dep2"n'
        '"dep1" -> "subdep1"n'
        '}'
    )
    
    assert content.strip() == expected_content.strip()

if __name__ == "__main__":
    pytest.main()
