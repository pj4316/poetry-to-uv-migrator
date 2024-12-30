import unittest

from migrate_poetry_to_uv import get_uv_dependencies
from tests.test_project_data import get_sample_poetry_pyproject_data, expected_uv_pyproject_data


class GetUVDependenciesTestCase(unittest.TestCase):
    def test_get_uv_dependencies(self):
        pyproject_data = get_sample_poetry_pyproject_data()
        result = get_uv_dependencies(pyproject_data)

        expected_dependencies = expected_uv_pyproject_data["project"]["dependencies"]
        for i, dependency in enumerate(expected_dependencies):
            self.assertEqual(result[i], dependency)
