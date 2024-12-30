import unittest

from poetry_to_uv_migrator.migrate_poetry_to_uv import convert_version


class ConvertVersionTestCase(unittest.TestCase):
    def test_convert_version_eq(self):
        version = "3.7"
        result = convert_version(version)
        self.assertEqual(result, "==3.7")

        version = "3.7.1"
        result = convert_version(version)
        self.assertEqual(result, "==3.7.1")

    def test_convert_version_ge(self):
        version = ">=3.7"
        result = convert_version(version)
        self.assertEqual(result, ">=3.7")

        version = ">=3.7.1"
        result = convert_version(version)
        self.assertEqual(result, ">=3.7.1")

    def test_convert_version_gt(self):
        version = ">3.7"
        result = convert_version(version)
        self.assertEqual(result, ">3.7")

        version = ">3.7.1"
        result = convert_version(version)
        self.assertEqual(result, ">3.7.1")

    def test_convert_version_le(self):
        version = "<=3.7"
        result = convert_version(version)
        self.assertEqual(result, "<=3.7")

        version = "<=3.7.1"
        result = convert_version(version)
        self.assertEqual(result, "<=3.7.1")

    def test_convert_version_lt(self):
        version = "<3.7"
        result = convert_version(version)
        self.assertEqual(result, "<3.7")

        version = "<3.7.1"
        result = convert_version(version)
        self.assertEqual(result, "<3.7.1")

    def test_convert_version_only(self):
        version = "~3.7"
        result = convert_version(version)
        self.assertEqual(result, ">=3.7.0,<3.8.0")

        version = "~3.7.1"
        result = convert_version(version)
        self.assertEqual(result, ">=3.7.1,<3.8.0")

    def test_convert_version_sementic(self):
        version = "^3.7"
        result = convert_version(version)
        self.assertEqual(result, ">=3.7.0,<4.0.0")

        version = "^3.7.1"
        result = convert_version(version)
        self.assertEqual(result, ">=3.7.1,<4.0.0")
