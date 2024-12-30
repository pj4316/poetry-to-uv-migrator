import unittest


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    # 특정 테스트 파일 추가
    suite.addTests(loader.discover("tests", pattern="*_test.py"))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(suite())