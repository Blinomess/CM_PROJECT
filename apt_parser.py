import re
import urllib.request
import urllib.error
from urllib.parse import urljoin
from errors import RepositoryError, DependencyVisualizerError

class APTParser:
    def __init__(self, repository_url, test_repo_mode=False):
        self.repository_url = repository_url
        self.test_repo_mode = test_repo_mode
        
    def get_package_dependencies(self, package_name):
        """Получить прямые зависимости пакета из APT репозитория"""
        try:
            if self.test_repo_mode:
                return self._get_dependencies_from_test_repo(package_name)
            else:
                return self._get_dependencies_from_ubuntu_repo(package_name)
                
        except urllib.error.URLError as e:
            raise RepositoryError(f"Ошибка доступа к репозиторию: {e}")
        except Exception as e:
            raise RepositoryError(f"Ошибка парсинга зависимостей: {e}")
    
    def _get_dependencies_from_ubuntu_repo(self, package_name):
        """Получить зависимости из официального репозитория Ubuntu"""
        # Формируем URL для Packages файла
        packages_url = urljoin(self.repository_url, "dists/focal/main/binary-amd64/Packages")
        
        # Скачиваем и парсим Packages файл
        with urllib.request.urlopen(packages_url) as response:
            content = response.read().decode('utf-8')
            
        return self._parse_packages_file(content, package_name)
    
    def _get_dependencies_from_test_repo(self, package_name):
        """Получить зависимости из тестового репозитория (файла)"""
        try:
            with open(self.repository_url, 'r', encoding='utf-8') as file:
                content = file.read()
            return self._parse_packages_file(content, package_name)
        except FileNotFoundError:
            raise RepositoryError(f"Файл репозитория не найден: {self.repository_url}")
        except IOError as e:
            raise RepositoryError(f"Ошибка чтения файла: {e}")
    
    def _parse_packages_file(self, content, target_package):
        """Парсинг файла Packages для поиска зависимостей"""
        packages = self._split_into_packages(content)
        
        for package_block in packages:
            if self._is_target_package(package_block, target_package):
                return self._extract_dependencies(package_block)
        
        raise RepositoryError(f"Пакет '{target_package}' не найден в репозитории")
    
    def _split_into_packages(self, content):
        """Разделить содержимое на блоки пакетов"""
        return re.split(r'\n\n', content.strip())
    
    def _is_target_package(self, package_block, target_package):
        """Проверить, является ли блок искомым пакетом"""
        package_match = re.search(r'^Package:\s*(.+)$', package_block, re.MULTILINE)
        return package_match and package_match.group(1) == target_package
    
    def _extract_dependencies(self, package_block):
        """Извлечь зависимости из блока пакета"""
        deps_match = re.search(r'^Depends:\s*(.+)$', package_block, re.MULTILINE)
        if not deps_match:
            return []  # Нет зависимостей
        
        depends_line = deps_match.group(1)
        return self._parse_depends_line(depends_line)
    
    def _parse_depends_line(self, depends_line):
        """Парсинг строки Depends для извлечения имен пакетов"""
        # Убираем версии и альтернативы (package1 | package2)
        dependencies = []
        for dep in depends_line.split(','):
            dep = dep.strip()
            # Извлекаем имя пакета (до первой скобки или конца)
            package_name = re.split(r'[\(\|]', dep)[0].strip()
            if package_name and package_name not in dependencies:
                dependencies.append(package_name)
        
        return dependencies