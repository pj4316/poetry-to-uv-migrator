import unittest

from poetry_to_uv_migrator.migrate_poetry_to_uv import convert_uv_project
from tests.test_project_data import get_sample_poetry_pyproject_data, expected_uv_pyproject_data


class ConvertVProjectSectionTestCase(unittest.TestCase):

    def test_get_uv_project_section(self):
        pyproject_data = get_sample_poetry_pyproject_data()
        result = convert_uv_project(pyproject_data)

        project_data = expected_uv_pyproject_data["project"]
        for key, value in result.items():
            self.assertEqual(value, project_data[key])
