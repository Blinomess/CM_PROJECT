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
        if "debian" in self.repository_url.lower():
            packages_url = urljoin(self.repository_url, "dists/stable/main/binary-amd64/Packages.gz")
        else:
            packages_url = "http://ftp.de.debian.org/debian/dists/stable/main/binary-amd64/Packages.gz"
        
        try:
            print(f"Загрузка файла Packages из: {packages_url}")
            with urllib.request.urlopen(packages_url, timeout=10) as response:
                import gzip
                content = gzip.decompress(response.read()).decode('utf-8')
                print("Файл Packages успешно загружен")
                
            return self._parse_packages_file(content, package_name)
        
        except urllib.error.URLError as e:
            raise RepositoryError(f"Ошибка сети: {e}")
        except Exception as e:
            raise RepositoryError(f"Ошибка загрузки зависимостей: {e}")
    
    def _get_dependencies_from_test_repo(self, package_name):
        try:
            with open(self.repository_url, 'r', encoding='utf-8') as file:
                content = file.read()
            return self._parse_packages_file(content, package_name)
        except FileNotFoundError:
            raise RepositoryError(f"Файл репозитория не найден: {self.repository_url}")
        except IOError as e:
            raise RepositoryError(f"Ошибка чтения файла: {e}")
    
    def _parse_packages_file(self, content, target_package):
        packages = self._split_into_packages(content)
        
        for package_block in packages:
            if self._is_target_package(package_block, target_package):
                return self._extract_dependencies(package_block)
        
        raise RepositoryError(f"Пакет '{target_package}' не найден в репозитории")
    
    def _split_into_packages(self, content):
        return re.split(r'\n\n', content.strip())
    
    def _is_target_package(self, package_block, target_package):
        package_match = re.search(r'^Package:\s*(.+)$', package_block, re.MULTILINE)
        return package_match and package_match.group(1) == target_package
    
    def _extract_dependencies(self, package_block):
        deps_match = re.search(r'^Depends:\s*(.+)$', package_block, re.MULTILINE)
        if not deps_match:
            return []
        
        depends_line = deps_match.group(1)
        return self._parse_depends_line(depends_line)
    
    def _parse_depends_line(self, depends_line):
        dependencies = []
        for dep in depends_line.split(','):
            dep = dep.strip()

            package_name = re.split(r'[\(\|]', dep)[0].strip()
            if package_name and package_name not in dependencies:
                dependencies.append(package_name)
        
        return dependencies