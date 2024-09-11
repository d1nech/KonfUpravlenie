import argparse
import os
import tarfile
import tempfile

# 1. Обработка аргументов командной строки
def parse_arguments():
    """Парсит аргументы командной строки."""
    parser = argparse.ArgumentParser(description='Shell Emulator')
    parser.add_argument('vfs_path', type=str, help='Path to the virtual filesystem archive (tar file)')
    return parser.parse_args()

# 2. Распаковка архива
def extract_vfs(vfs_path):
    """Извлекает виртуальную файловую систему из tar-архива."""
    temp_dir = tempfile.mkdtemp()  # Создание временной директории
    with tarfile.open(vfs_path, 'r') as tar:
        tar.extractall(temp_dir)  # Извлечение содержимого архива
    return temp_dir

# 3. Реализация команд
def ls(current_dir):
    """Возвращает список файлов и директорий в текущей директории."""
    return os.listdir(current_dir)

def cd(current_dir, new_dir):
    """Изменяет текущую директорию на новую."""
    new_path = os.path.join(current_dir, new_dir)
    if os.path.isdir(new_path):
        return new_path
    else:
        raise FileNotFoundError(f"{new_dir} not found")

def exit_emulator():
    """Выход из эмулятора."""
    print("Exiting emulator.")
    exit(0)

def whoami():
    """Возвращает имя текущего пользователя."""
    return os.getlogin()

def mv(source, destination):
    """Перемещает файл или директорию из source в destination."""
    os.rename(source, destination)

def tree(directory):
    """Рекурсивно отображает структуру директорий."""
    result = []
    for root, dirs, files in os.walk(directory):
        level = root.replace(directory, '').count(os.sep)
        indent = ' ' * 4 * (level)
        result.append(f"{indent}{os.path.basename(root)}/")
        for f in files:
            result.append(f"{indent}    {f}")
    return "\n".join(result)

# 4. Запуск эмулятора
if __name__ == "__main__":
    args = parse_arguments()  # Парсинг аргументов
    vfs_path = args.vfs_path
    
    current_dir = extract_vfs(vfs_path)  # Извлечение виртуальной файловой системы
    
    print(f"Welcome to the Shell Emulator! Current directory: {current_dir}\n")
    
    while True:
        command = input(f"{current_dir}> ")  # Ввод команды от пользователя
        
        try:
            if command.startswith("ls"):
                output = ls(current_dir)
                print("\n".join(output))
            elif command.startswith("cd "):
                _, new_dir = command.split(maxsplit=1)
                current_dir = cd(current_dir, new_dir)
                print(f"Changed directory to: {current_dir}")
            elif command == "exit":
                break
            elif command == "whoami":
                output = whoami()
                print(output)
            elif command.startswith("mv "):
                _, source, destination = command.split(maxsplit=2)
                mv(source, destination)
                print(f"Moved {source} to {destination}")
            elif command.startswith("tree"):
                output = tree(current_dir)
                print(output)
            else:
                print(f"Command not found: {command}")
        except Exception as e:
            print(str(e))
