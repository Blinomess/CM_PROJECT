<h1>Общее описание:</h1>
Dependency Visualizer - это CLI-приложение для анализа и визуализации графа зависимостей пакетов в репозиториях Ubuntu/Debian. Приложение поддерживает как работу с реальными репозиториями, так и тестовыми данными.

<h1>Основные возможности:</h1>
- Анализ прямых и транзитивных зависимостей пакетов
- Построение графа зависимостей с помощью DFS алгоритма
- Ограничение глубины анализа
- Фильтрация пакетов по имени
- Обнаружение и обработка циклических зависимостей
- Визуализация в формате ASCII-дерева
- Поддержка тестового режима с пакетами-заглушками

<h1>Описание всех функций и настроек:</h1>
- main.py: Основной модуль приложения
- parser.py: Парсинг командной строки
- config.py: Конфигурация и валидация
- errors.py: Пользовательские исключения
- apt_parser.py: Парсер APT репозиториев
- graph_builder.py: Построитель графа зависимостей
- test_repository.py: Работа с тестовыми репозиториями
- test_repo.txt: Пример тестового репозитория

<h1>Модули и их функции:</h1>
<h2>main.py</h2>
- DependencyVisualizer: основной класс приложения
- analyze_dependencies(): основной метод анализа
- _display_dependency_info(): вывод информации о графе
- _display_ascii_tree(): визуализация дерева зависимостей

<h2>parser.py</h2>
- CommandLineParser: парсинг аргументов командной строки
- Поддержка всех необходимых флагов и параметров

<h2>config.py</h2>
- Config: хранение и валидация конфигурации
- Валидация URL и параметров

<h2>apt_parser.py</h2>
- APTParser: работа с APT репозиториями
- get_package_dependencies(): получение зависимостей пакета

<h2>graph_builder.py</h2>
- GraphBuilder: построение графа зависимостей
- build_dependency_graph(): основной метод построения
- _dfs(): рекурсивный DFS обход
- Обнаружение циклических зависимостей

<h2>test_repository.py</h2>
- TestRepository: работа с тестовыми репозиториями
- Поддержка пакетов, обозначенных большими латинскими буквами

<h1>Флаги:</h1>
- Имя пакета
- URL репозитория
- Режим тестирования: "--test-repo-mode"
- Файл вывода: "--output"
- ASCII-дерево: "--ascii-tree"
- Макс. глубина: "--max-depth"
- Фильтр "--filter"

<h1>Команды для сборки и запуска тестов</h1>

<h2>Требования:</h2>
- Python 3.6+
- Доступ к интернету (для работы с реальными репозиториями)

<h2>Вариации запуска приложения:</h2>

```bash
# Базовая команда
python main.py <package_name> <repository_url> [options]

# С реальным репозиторием + аски дерево
python main.py python3 http://ftp.de.debian.org/debian/ --ascii-tree

# С тестовым репозиторием + аски дерево
python main.py A test_repo.txt --test-repo-mode --ascii-tree

# С ограничением глубины = 2
python main.py A test_repo.txt --test-repo-mode --max-depth 2

# С фильтрацией пакетов = "C"
python main.py A test_repo.txt --test-repo-mode --filter "C"
```

<h1>Пример тестового файла</h1>

```
Package: A
Depends: B, C

Package: B
Depends: D, E

Package: C
Depends: F, G

Package: D
Depends: H

Package: E
Depends: 

Package: F
Depends: A, H  # Циклическая зависимость
```

<h1>Запуск программы</h2>
```
PS C:\Users\kolyb\Desktop\CM\cm2\CM_PROJECT> python main.py A test_repo.txt --test-repo-mode --ascii-tree
```

<h1>Вывод программы</h1>
```
Конфигурация:
package_name: A
repository_url: test_repo.txt
test_repo_mode: True
output_filename: dependency_graph.png
ascii_tree_mode: True
max_depth: None
filter_substring: None

Детальный граф зависимостей:
  A -> B, C
  B -> D, E
  D -> H
  H -> (нет зависимостей)
  E -> (нет зависимостей)
  C -> F, G
  F -> A, H
  G -> I
  I -> J
  J -> (нет зависимостей)

Дерево зависимостей 'A':
L A
    Г B
    |   Г D
    |   |   L H
    |   L E
    L C
        Г F
        |   Г A [ЦИКЛ]
        |   L H
        L G
            L I
                L J

Завершено успешно!
```

<h1>Особенности реализации:</h1>
- Настраиваемое CLI - приложение
- Формат пакетов: Ubuntu (apt)
- Извлечение информации пакета через URL репозиторий
- DFS с рекурсией - граф строится с помощью глубинного поиска
- Обработка циклов - обнаружение и маркировка циклических зависимостей
- Фильтрация - исключение пакетов по подстроке на этапе построения графа
- Ограничение глубины - остановка рекурсии при достижении максимальной глубины
- Тестовый режим - работа с упрощенными пакетами для демонстрации