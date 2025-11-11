from errors import DependencyVisualizerError, RepositoryError

class GraphBuilder:
    def __init__(self, apt_parser, max_depth=None, filter_substring=None):
        self.apt_parser = apt_parser
        self.max_depth = max_depth
        self.filter_substring = filter_substring
        self.visited = set()
        self.recursion_stack = set()
        self.dependency_graph = {}
        self.cyclic_dependencies = set()
        self.cyclic_packages = set()
        
    def build_dependency_graph(self, package_name):
        self.visited.clear()
        self.recursion_stack.clear()
        self.dependency_graph.clear()
        self.cyclic_dependencies.clear()
        self.cyclic_packages.clear()
        self._dfs(package_name, 0)
        return self.dependency_graph
    
    def _dfs(self, package_name, current_depth):
        if self.max_depth and current_depth >= self.max_depth:
            return
            
        if self.filter_substring and self.filter_substring in package_name:
            return
            
        if package_name in self.recursion_stack:
            self.cyclic_dependencies.add(package_name)
            self.cyclic_packages.add(package_name)
            return
            
        if package_name in self.visited:
            return
            
        self.visited.add(package_name)
        self.recursion_stack.add(package_name)
        
        try:
            dependencies = self.apt_parser.get_package_dependencies(package_name)
            self.dependency_graph[package_name] = dependencies
            
            for dep in dependencies:
                self._dfs(dep, current_depth + 1)
                
        except RepositoryError as e:
            if package_name not in self.dependency_graph:
                self.dependency_graph[package_name] = []
            print(f"{e}")
            
        finally:
            self.recursion_stack.remove(package_name)
    
    @property
    def has_cyclic_dependencies(self):
        return len(self.cyclic_dependencies) > 0
    
    def get_cyclic_dependencies(self):
        return self.cyclic_dependencies.copy()
    
    def get_flattened_dependencies(self):
        all_deps = set()
        for package, deps in self.dependency_graph.items():
            all_deps.update(deps)
        return sorted(all_deps)
    
    def get_dependency_count(self):
        return len(self.get_flattened_dependencies())
    
    def get_package_count(self):
        return len(self.dependency_graph)
    
    def get_root_dependencies(self, package_name):
        return self.dependency_graph.get(package_name, [])
    
    def get_graph_statistics(self):
        total_packages = self.get_package_count()
        total_dependencies = self.get_dependency_count()
        has_cycles = self.has_cyclic_dependencies
        
        return {
            'total_packages': total_packages,
            'total_dependencies': total_dependencies,
            'has_cyclic_dependencies': has_cycles,
            'cyclic_packages_count': len(self.cyclic_dependencies)
        }