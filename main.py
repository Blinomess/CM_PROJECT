import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from parser import CommandLineParser
from errors import DependencyVisualizerError, ValidationError, ConfigError, RepositoryError
from apt_parser import APTParser
from graph_builder import GraphBuilder

class DependencyVisualizer:
    def __init__(self, config):
        self.config = config
        self.apt_parser = APTParser(config.repository_url, config.test_repo_mode)
        self.graph_builder = GraphBuilder(
            self.apt_parser, 
            config.max_depth, 
            config.filter_substring
        )

    def display_config(self):
        print("Конфигурация:")
        print(self.config)

    def analyze_dependencies(self):
        try:
            dependency_graph = self.graph_builder.build_dependency_graph(
                self.config.package_name
            )

            self._display_dependency_graph(dependency_graph)

            if self.config.ascii_tree_mode:
                self._display_ascii_tree(dependency_graph)
            
            return dependency_graph
            
        except RepositoryError as e:
            raise

    def _display_dependency_graph(self, graph):
        if not graph:
            print("Граф зависимостей пуст")
            return
        
        print(f"\nДетальный граф зависимостей:")
        for package, dependencies in graph.items():
            if dependencies:
                deps_str = ", ".join(dependencies)
                print(f"  {package} -> {deps_str}")
            else:
                print(f"  {package} -> (нет зависимостей)")
    
    def _display_ascii_tree(self, graph):
        print(f"\nДерево зависимостей '{self.config.package_name}':")
        if self.config.package_name not in graph:
            print("  Пакет не найден в графе")
            return
            
        visited = set()
        self._print_tree_node(self.config.package_name, graph, "", True, visited)
    
    def _print_tree_node(self, package, graph, prefix, is_last, visited):
        if package in visited:
            connector = "L " if is_last else "Г "
            print(prefix + connector + package + " [ЦИКЛ]")
            return
            
        visited.add(package)
        
        connector = "L " if is_last else "Г "
        print(prefix + connector + package)
        
        if package in graph:
            dependencies = graph[package]
            new_prefix = prefix + ("    " if is_last else "|   ")
            
            for i, dep in enumerate(dependencies):
                is_last_dep = (i == len(dependencies) - 1)
                self._print_tree_node(dep, graph, new_prefix, is_last_dep, visited.copy())

def main():
    try:
        parser = CommandLineParser()
        config = parser.parse_args()
        
        visualizer = DependencyVisualizer(config)
        
        visualizer.display_config()
        
        dependency_graph = visualizer.analyze_dependencies()

        print(f"\nЗавершено успешно!")
        
    except ValidationError as e:
        print(f"Ошибка валидации: {e}", file=sys.stderr)
        sys.exit(1)
    except ConfigError as e:
        print(f"Ошибка конфигурации: {e}", file=sys.stderr)
        sys.exit(1)
    except RepositoryError as e:
        print(f"Ошибка репозитория: {e}", file=sys.stderr)
        sys.exit(1)
    except DependencyVisualizerError as e:
        print(f"Ошибка визуализатора: {e}", file=sys.stderr)
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nПрервано пользователем", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Неожиданная ошибка: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()