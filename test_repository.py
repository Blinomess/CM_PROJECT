from errors import RepositoryError

class TestRepository:
    def __init__(self, file_path):
        self.file_path = file_path
        self.packages_data = self._load_test_repository()
    
    def _load_test_repository(self):
        """Загрузить данные тестового репозитория из файла"""
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return self._parse_test_repository(content)
        except FileNotFoundError:
            raise RepositoryError(f"Тестовый репозиторий не найден: {self.file_path}")
        except IOError as e:
            raise RepositoryError(f"Ошибка чтения тестового репозитория: {e}")
    
    def _parse_test_repository(self, content):
        """Парсинг тестового репозитория"""
        packages = {}
        package_blocks = content.strip().split('\n\n')
        
        for block in package_blocks:
            package_name = None
            dependencies = []
            
            for line in block.split('\n'):
                line = line.strip()
                if line.startswith('Package:'):
                    package_name = line.split(':', 1)[1].strip()
                elif line.startswith('Depends:'):
                    deps_str = line.split(':', 1)[1].strip()
                    if deps_str:
                        dependencies = [dep.strip() for dep in deps_str.split(',')]
            
            if package_name:
                packages[package_name] = dependencies
        
        return packages
    
    def get_package_dependencies(self, package_name):
        """Получить зависимости пакета из тестового репозитория"""
        if package_name not in self.packages_data:
            raise RepositoryError(f"Пакет '{package_name}' не найден в тестовом репозитории")
        
        return self.packages_data[package_name]