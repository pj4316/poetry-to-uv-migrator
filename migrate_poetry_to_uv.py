import os
import re
from collections import OrderedDict

import toml


def convert_author(author_str):
    if not isinstance(author_str, str):
        return {}

    match = re.match(r"(?P<name>[^<]+) <(?P<email>[^>]+)>", author_str)
    if match:
        return {
            "name": match.group("name").strip(),
            "email": match.group("email").strip(),
        }
    return {}


def convert_version(version):
    if isinstance(version, dict):
        # if dependency from source directory
        return ""

    tilde_match = re.match(r"~(\d+)\.(\d+)(?:\.(\d+))?", version)
    caret_match = re.match(r"\^(\d+)\.(\d+)(?:\.(\d+))?", version)

    if tilde_match:
        major, minor, patch = tilde_match.groups(default="0")
        next_minor = int(minor) + 1
        return f">={major}.{minor}.{patch},<{major}.{next_minor}.0"

    elif caret_match:
        major, minor, patch = caret_match.groups(default="0")
        if major == "0":
            if minor == "0":
                next_patch = int(patch) + 1
                return f">={major}.{minor}.{patch},<{major}.{minor}.{next_patch}"
            next_minor = int(minor) + 1
            return f">={major}.{minor}.{patch},<{major}.{next_minor}.0"
        next_major = int(major) + 1
        return f">={major}.{minor}.{patch},<{next_major}.0.0"
    elif version.startswith(">") or version.startswith("<"):
        return version
    else:
        return f"=={version}"


def convert_uv_project(pyproject_data):
    poetry_data = pyproject_data.get("tool", {}).get("poetry", {})
    project = OrderedDict(
        [
            ("name", ""),
            ("version", ""),
            ("description", ""),
            ("readme", ""),
            ("authors", []),
            ("dependencies", []),
        ]
    )
    project["name"] = poetry_data.get("name", "")
    project["version"] = poetry_data.get("version", "")
    project["description"] = poetry_data.get("description", "")
    if "readme" in poetry_data:
        project["readme"] = poetry_data["readme"]
    if "authors" in poetry_data:
        authors = []
        for author in poetry_data["authors"]:
            authors.append(convert_author(author))
        project["authors"] = authors

    project["dependencies"] = convert_uv_dependencies(pyproject_data)

    poetry_dependencies = (
        pyproject_data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    )

    if poetry_dependencies.get("python", "") != "":
        project["requires-python"] = convert_version(poetry_dependencies["python"])
    return project


def convert_uv_dependencies(pyproject_data):
    poetry_dependencies = (
        pyproject_data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    )
    project_dependencies = []
    for package, version in poetry_dependencies.items():
        if package != "python":
            project_dependencies.append(f"{package}{convert_version(version)}")
    return project_dependencies


def convert_tool_uv(pyproject_data):
    tool_uv = {
        "uv": OrderedDict(
            [
                ("sources", {}),
            ]
        )
    }
    poetry_dependencies = (
        pyproject_data.get("tool", {}).get("poetry", {}).get("dependencies", {})
    )
    uv_sources = {}
    for package, version in poetry_dependencies.items():
        if isinstance(version, dict):
            uv_sources[package] = {"path": version["path"]}

    tool_uv["uv"]["sources"] = uv_sources

    index = []
    tool_poetry_source = (
        pyproject_data.get("tool", {}).get("poetry", {}).get("source", [])
    )

    if tool_poetry_source:
        for source in tool_poetry_source:
            if "priority" in source and source["priority"] == "primary":
                source["default"] = True
                del source["priority"]
            index.append(source)

    if len(index) > 0:
        tool_uv["uv"]["index"] = index
    return tool_uv


def convert_build_system(pyproject_data):
    poetry_data = pyproject_data.get("build-system", {})
    return {
        "requires", ["hatchling"],
        "build-backend", "hatchling.build",
    } if poetry_data["build-backend"] == "poetry.core.masonry.api" else {
        "requires", ["setuptools>=70"],
        "build-backend", "setuptools.build_meta",
    }


def remove_empty_sections(data):
    """Recursively remove empty sections from a dictionary."""
    keys_to_remove = []
    for key, value in data.items():
        if isinstance(value, dict):
            remove_empty_sections(value)
            if not value:  # If the dictionary is empty after recursion
                keys_to_remove.append(key)
    for key in keys_to_remove:
        del data[key]


def remove_poetry_sections(data):
    """Remove poetry sections from a dictionary."""
    if "tool" in data and "poetry" in data["tool"]:
        del data["tool"]["poetry"]


def migrate_pyproject_to_uv(path):
    pyproject_path = path

    with open(pyproject_path, "r") as file:
        pyproject_data = toml.load(file)

    if "tool" not in pyproject_data or "poetry" not in pyproject_data["tool"]:
        print(f"Skipping {pyproject_path} as it does not contain a poetry section")
        return

    uv_pyproject_data = OrderedDict(
        [
            (
                "project",
                OrderedDict(
                    [
                        ("name", ""),
                        ("version", ""),
                        ("description", ""),
                        ("readme", ""),
                        ("authors", []),
                        ("dependencies", []),
                    ]
                ),
            ),
            ("tool", {"uv": OrderedDict([("sources", {}), ("index", [])])}),
            ("build-system", {}),
        ]
    )

    uv_pyproject_data["project"] = convert_uv_project(pyproject_data)
    uv_pyproject_data["tool"] = convert_tool_uv(pyproject_data)
    uv_pyproject_data["build-system"] = convert_build_system(pyproject_data)

    remove_empty_sections(uv_pyproject_data)

    with open(path, "w") as file:
        toml.dump(uv_pyproject_data, file)

    print(f"Converted UV pyproject.toml saved to {path}")


def find_and_migrate_pyprojects(directory, exclude_root=False):
    exclude_dirs = {"node_modules", ".next", ".venv"}
    pyproject_paths = []
    for root, dirs, files in os.walk(directory):
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        if exclude_root and os.path.abspath(root) == os.path.abspath(directory):
            continue
        for file in files:
            if file == "pyproject.toml":
                pyproject_path = os.path.join(root, file)
                pyproject_paths.append(os.path.abspath(pyproject_path))
    return pyproject_paths


if __name__ == "__main__":
    paths = find_and_migrate_pyprojects("../", True)

    for path in paths:
        migrate_pyproject_to_uv(path)
    # for path in paths:
    # migrate_pyproject_to_uv(path)
