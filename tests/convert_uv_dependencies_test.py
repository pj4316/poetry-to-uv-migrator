import unittest

from migrate_poetry_to_uv import convert_uv_dependencies
from tests.test_project_data import get_sample_poetry_pyproject_data, expected_uv_pyproject_data


class ConvertUVDependenciesTestCase(unittest.TestCase):
    def test_get_uv_dependencies(self):
        pyproject_data = get_sample_poetry_pyproject_data()
        result = convert_uv_dependencies(pyproject_data)

        expected_dependencies = expected_uv_pyproject_data["project"]["dependencies"]
        for i, dependency in enumerate(expected_dependencies):
            self.assertEqual(result[i], dependency)
