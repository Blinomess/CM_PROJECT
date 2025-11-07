import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parser import CommandLineParser
from errors import DependencyVisualizerError, ValidationError, ConfigError, RepositoryError
from apt_parser import APTParser

class DependencyVisualizer:
    def __init__(self, config):
        self.config = config
        self.apt_parser = APTParser(config.repository_url, config.test_repo_mode)

    def display_config(self):
        print("Конфигурация:")
        print(self.config)

    def analyze_dependencies(self):
        """Анализ зависимостей пакета - новая функция из этапа 2"""
        print(f"\nАнализа зависимостей для пакета: {self.config.package_name}")
        print(f"Репозиторий: {self.config.repository_url}")
        
        try:
            # Получаем прямые зависимости - новая логика этапа 2
            dependencies = self.apt_parser.get_package_dependencies(self.config.package_name)
            
            # Вывод зависимостей (требование этапа 2)
            self._display_dependencies(dependencies)
            
            # Фильтрация если указана подстрока
            if self.config.filter_substring:
                dependencies = [dep for dep in dependencies 
                              if self.config.filter_substring in dep]
                print(f"\nПосле фильтрации по '{self.config.filter_substring}':")
                self._display_dependencies(dependencies)
            
            # ASCII-дерево если активировано
            if self.config.ascii_tree_mode:
                self._display_ascii_tree(dependencies)
            
            return dependencies
            
        except RepositoryError as e:
            raise
    
    def _display_dependencies(self, dependencies):
        """Вывод списка зависимостей - новая функция из этапа 2"""
        if not dependencies:
            print("Пакет не имеет зависимостей")
            return
        
        print(f"\nПрямые зависимости пакета '{self.config.package_name}':")
        for i, dep in enumerate(dependencies, 1):
            print(f"  {i}. {dep}")
        print(f"Всего зависимостей: {len(dependencies)}")
    
    def _display_ascii_tree(self, dependencies):
        """Отображение ASCII-дерева зависимостей - обновленная функция"""
        print(f"\nДерево зависимостей '{self.config.package_name}':")
        if not dependencies:
            print("  └── (нет зависимостей)")
            return
        
        for i, dep in enumerate(dependencies):
            if i == len(dependencies) - 1:
                print(f"  └── {dep}")
            else:
                print(f"  ├── {dep}")
    
    def simulate_dependency_analysis(self):
        print(f"\nАнализа зависимостей для пакета: {self.config.package_name}\n")
        
        if self.config.test_repo_mode:
            print("Тестовый репозиторий")
        else:
            print("Реальный репозиторий")
        
        if self.config.max_depth:
            print(f"Максимальная глубина: {self.config.max_depth}")
        
        if self.config.filter_substring:
            print(f"Фильтр пакетов: '{self.config.filter_substring}'")
        
        if self.config.ascii_tree_mode:
            print("\nАски дерево: ")
            self._display_sample_ascii_tree()
        
        print(f"\nРезультат сохранён в: {self.config.output_filename}")
    
    def _display_sample_ascii_tree(self):
        sample_tree = """
sample-package-1.0.0
├── dependency-a-2.1.0
│   ├── sub-dependency-x-1.0.0
│   └── sub-dependency-y-1.5.0
├── dependency-b-3.0.0
│   └── sub-dependency-z-2.0.0
└── dependency-c-1.2.0
            """
        print(sample_tree)

def main():
    try:
        parser = CommandLineParser()
        config = parser.parse_args()
        
        visualizer = DependencyVisualizer(config)
        
        visualizer.display_config()
        
        dependencies = visualizer.analyze_dependencies()
        
        print(f"\nЗавершено. Найдено {len(dependencies)} зависимостей")
        
    except ValidationError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except ConfigError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except RepositoryError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except DependencyVisualizerError as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nОтмена", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()