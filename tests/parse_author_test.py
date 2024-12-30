import unittest

from migrate_poetry_to_uv import parse_author
from tests.test_project_data import get_sample_poetry_pyproject_data


class ParseAuthorTestCase(unittest.TestCase):
    def test_parse_author(self):
        project_data = get_sample_poetry_pyproject_data()

        author = project_data["tool"]["poetry"]["authors"][0]
        result = parse_author(author)

        self.assertEqual(result["name"], "Max Lee")
        self.assertEqual(result["email"], "pj4316@naver.com")

    def test_return_empty_dict_if_author_is_empty(self):
        author = ""
        result = parse_author(author)
        self.assertEqual(result, {})
