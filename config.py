from errors import ValidationError

class Config:
    def __init__(self):
        self.package_name = None
        self.repository_url = None
        self.test_repo_mode = False
        self.output_filename = "dependency_graph.png"
        self.ascii_tree_mode = False
        self.max_depth = None
        self.filter_substring = None

    def validate(self):
        errors = []
        
        if not self.package_name:
            errors.append("Имя обязательно")
        
        if not self.repository_url:
            errors.append("Путь обязателен")

        if not self.test_repo_mode:
            if not self._is_valid_url(self.repository_url):
                errors.append(f"Некорректный URL репозитория: {self.repository_url}")
        
        if self.max_depth is not None:
            if not isinstance(self.max_depth, int) or self.max_depth < 1:
                errors.append("Глубина должна быть положительной")
        
        if errors:
            raise ValidationError("; ".join(errors))

    def __str__(self):
        config_items = [
            f"package_name: {self.package_name}",
            f"repository_url: {self.repository_url}",
            f"test_repo_mode: {self.test_repo_mode}",
            f"output_filename: {self.output_filename}",
            f"ascii_tree_mode: {self.ascii_tree_mode}",
            f"max_depth: {self.max_depth}",
            f"filter_substring: {self.filter_substring}"
        ]
        return "\n".join(config_items)
    
    def _is_valid_url(self, url):
        try:
            from urllib.parse import urlparse
            result = urlparse(url)
            return all([result.scheme, result.netloc])
        except Exception:
            return False