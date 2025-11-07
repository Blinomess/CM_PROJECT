import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parser import CommandLineParser
from errors import DependencyVisualizerError, ValidationError, ConfigError, RepositoryError

class DependencyVisualizer:
    def __init__(self, config):
        self.config = config
    
    def display_config(self):
        print("Конфигурация:")
        print(self.config)
    
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
        
        visualizer.simulate_dependency_analysis()
        
        
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
        print("\Отмена", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()