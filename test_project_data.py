import os

import toml

expected_poetry_pyproject_data = {
    "tool": {
        "poetry": {
            "name": "sample-project",
            "version": "0.0.1",
            "description": "sample description",
            "readme": "README.md",
            "authors": ["Max Lee <pj4316@naver.com>"],
            "dependencies": {
                "python": "~3.10",
                "dependency-injector": "^4.41.0",
                "fastapi": ">=0.111.0,<0.112.0",
                "pydantic": "^2.5.3",
                "uvicorn": "~0.30.1",
                "libary1": {"path": "library/libary1", "develop": True},
                "libary2": {"path": "library/libary2", "develop": True},

            },
            "source": [
                {
                    "name": "pypi",
                    "url": "https://pypi.org/simple",
                    "priority": "primary",
                }
            ],
        }
    },
    "build-system": {
        "requires": ["poetry-core"],
        "build-backend": "poetry.core.masonry.api",
    }
}

expected_uv_pyproject_data = {
    "project": {
        "name": "sample-project",
        "version": "0.0.1",
        "description": "sample description",
        "readme": "README.md",
        "authors": [{"name": "Max Lee", "email": "pj4316@naver.com"}],
        "dependencies": [
            "dependency-injector>=4.41.0,<5.0.0",
            "fastapi>=0.111.0,<0.112.0",
            "pydantic>=2.5.3,<3.0.0",
            "uvicorn>=0.30.1,<0.31.0",
            "libary1",
            "libary2"
        ],
        "requires-python": ">=3.10.0,<3.11.0",
    },
    "tool": {
        "uv": {
            "sources": {
                "libary1": {"path": "library/libary1"},
                "libary2": {"path": "library/libary2"},
            },
            "index": [
                {
                    "name": "pypi",
                    "url": "https://pypi.org/simple",
                    "default": True,
                }
            ]
        }
    },
    "build-system": {
        "requires": ["setuptools>=70"],
        "build-backend": "setuptools.build_meta",
    }
}


def get_sample_poetry_pyproject_data():
    pyproject_path = "tests/sample_poetry_pyproject.toml"
    with open(pyproject_path, "r") as file:
        pyproject_data = toml.load(file)
    return pyproject_data


def validate_sample():
    pyproject_data = get_sample_poetry_pyproject_data()
    assert pyproject_data == expected_poetry_pyproject_data
