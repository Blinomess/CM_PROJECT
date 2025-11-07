class DependencyVisualizerError(Exception):
    pass

class ConfigError(DependencyVisualizerError):
    pass

class ValidationError(DependencyVisualizerError):
    pass

class RepositoryError(DependencyVisualizerError):
    pass