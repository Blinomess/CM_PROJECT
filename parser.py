import argparse
import sys
from config import Config
from errors import ValidationError

class CommandLineParser:
    def __init__(self):
        self.parser = self._setup_parser()
    
    def _setup_parser(self):
        parser = argparse.ArgumentParser(
            description="Визуализация графа зависимостей пакетов",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog="""
Примеры:
python main.py numpy https://pypi.org/project/numpy/
python main.py requests /local/repo --test-repo-mode --max-depth 2 --ascii-tree
python main.py django /path/to/repo --filter "security" --output deps.png
            """
        )
        
        parser.add_argument(
            'package_name',
            type=str,
            help='Имя пакета'
        )
        
        parser.add_argument(
            'repository_url',
            type=str,
            help='URL репозитория или путь к файлу'
        )
        
        parser.add_argument(
            '--test-repo-mode',
            action='store_true',
            default=False,
            help='Тестовый репозиторий'
        )
        
        parser.add_argument(
            '--output',
            '-o',
            type=str,
            default='dependency_graph.png',
            help='Имя файла с изображением графа'
        )
        
        parser.add_argument(
            '--ascii-tree',
            action='store_true',
            default=False,
            help='Аски дерево'
        )
        
        parser.add_argument(
            '--max-depth',
            '-d',
            type=int,
            help='Глубина анализа зависимостей'
        )
        
        parser.add_argument(
            '--filter',
            '-f',
            type=str,
            help='Подстрока для фильтрации пакетов'
        )
        
        return parser
    
    def parse_args(self, args=None):
        try:
            parsed_args = self.parser.parse_args(args)
            
            config = Config()
            config.package_name = parsed_args.package_name
            config.repository_url = parsed_args.repository_url
            config.test_repo_mode = parsed_args.test_repo_mode
            config.output_filename = parsed_args.output
            config.ascii_tree_mode = parsed_args.ascii_tree
            config.max_depth = parsed_args.max_depth
            config.filter_substring = parsed_args.filter
            
            config.validate()
            
            return config
            
        except SystemExit:
            sys.exit(1)
        except Exception as e:
            if hasattr(e, '__module__') and e.__module__ == 'argparse':
                sys.exit(1)
            raise ValidationError(f"{str(e)}")