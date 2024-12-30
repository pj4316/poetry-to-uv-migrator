# Poetry to UV pyproject file migrator

This script converts a `pyproject.toml` file for [poetry](https://python-poetry.org/) to a `pyproject.toml` file for [uv](https://docs.astral.sh/uv/).
This script is only for the `pyproject.toml` file, not for the entire project.


# Convert What?

- 📝 **project description**: `tool.poetry` section to `project` section of uv.
- 🔗 **dependencies**: `tool.poetry.dependencies` section to `project.dependencies` section of uv.
- 🌐 **sources**: `tool.poetry.sources` section to `tool.uv.sources` section of uv.
- 🛠️ **build-system**: `build-system` section to `build-system` section of uv.
- 🔒 **private index**: `tool.poetry.source` to `tool.uv.index` section of uv.

# How to use?

just call the method to migrate poetry to uv

example
```python
if __name__ == '__main__':
    your_project_pyproject = '/path/to/your-project/pyproject.toml'
    migrate_pyproject_to_uv(your_project_pyproject) 
```

If you want to migrate to all directories recursively below the path, please follow below
```python
if __name__ == "__main__":
    your_project_path_root = '/path/to/your-project'
    paths = find_and_migrate_pyprojects("your_project_path_root", True)

    for path in paths:
        migrate_pyproject_to_uv(path)
```
