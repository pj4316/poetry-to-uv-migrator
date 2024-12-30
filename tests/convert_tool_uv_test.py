import unittest

from migrate_poetry_to_uv import convert_tool_uv
from tests.test_project_data import get_sample_poetry_pyproject_data, expected_uv_pyproject_data


class ConvertToolUVTestCase(unittest.TestCase):
    def test_local_source(self):
        pyproject_data = get_sample_poetry_pyproject_data()
        result = convert_tool_uv(pyproject_data)

        expected_sources = expected_uv_pyproject_data["tool"]["uv"]["sources"]
        for key, value in result["uv"]["sources"].items():
            self.assertEqual(value, expected_sources[key])

    def test_index(self):
        pyproject_data = get_sample_poetry_pyproject_data()
        result = convert_tool_uv(pyproject_data)

        expected_index = expected_uv_pyproject_data["tool"]["uv"]["index"]
        self.assertEqual(result["uv"]["index"], expected_index)