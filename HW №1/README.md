# Домашнее задание №1 Вариант 14
___
## Описание
Этот проект представляет собой эмулятор командной оболочки, который позволяет взаимодействовать с виртуальной файловой системой (VFS), упакованной в архив .tar. С помощью этого эмулятора вы можете выполнять различные команды для управления файлами и директориями внутри VFS.
___
## Запуск программы
Чтобы запустить эмулятор, используйте следующую команду, указывая путь к вашему архиву VFS: `python shell_emulator.py <vfs_path>
` Где <vfs_path> — это путь к вашему архиву .tar.
## Использование
- ls — показать содержимое текущей директории.
- cd <directory> — сменить текущую директорию.
- exit — выйти из эмулятора.
- whoami — показать имя текущего пользователя.
- mv <source> <destination> — переместить файл или директорию.
- tree — отобразить структуру директорий.
___
## Тестирование с помощью Pytest
![pytest](https://github.com/d1nech/KonfUpravlenie/blob/main/HW%20№1/testimg/Снимок%20экрана%202024-09-17%20183759.png?raw=true)
___
## Тестирование
### Запуск программы
![zapusk](https://github.com/d1nech/KonfUpravlenie/blob/main/HW%20№1/testimg/zapusk.png?raw=true)
### Команда ls
![ls](https://github.com/d1nech/KonfUpravlenie/blob/main/HW%20№1/testimg/ls.png?raw=true)
### Команда cd
![cd](https://github.com/d1nech/KonfUpravlenie/blob/main/HW%20№1/testimg/cd.png?raw=true)
### Команда whoami
![whoami](https://github.com/d1nech/KonfUpravlenie/blob/main/HW%20№1/testimg/whoami.png?raw=true)
### Команда tree
![tree](https://github.com/d1nech/KonfUpravlenie/blob/main/HW%20№1/testimg/tree.png?raw=true)
### Команда mv
![mv](https://github.com/d1nech/KonfUpravlenie/blob/main/HW%20№1/testimg/mv.png?raw=true)
![resultmv](https://github.com/d1nech/KonfUpravlenie/blob/main/HW%20№1/testimg/resultmv.png?raw=true)
___
## GUI
### Выбираем виртуальную файловую систему
![GUIstart](https://github.com/d1nech/KonfUpravlenie/blob/main/HW%20№1/testimg/Снимок%20экрана%202024-09-17%20180316.png?raw=true)
### Тестирование команд ls,whoami,tree
![GUItest](https://github.com/d1nech/KonfUpravlenie/blob/main/HW%20№1/testimg/Снимок%20экрана%202024-09-17%20180335.png?raw=true)
