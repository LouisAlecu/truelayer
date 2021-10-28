import test_dataset_cleaner
import test_app
import unittest


def run_tests() -> None:
    """
    Orchestrates all the tests
    """
    tests = {
        "test_dataset_cleaner": test_dataset_cleaner.suite,
        "test_app": test_app.suite,
    }
    runner = unittest.TextTestRunner()
    for test in tests:
        print(test)
        runner.run(tests[test]())


if __name__ == "__main__":
    run_tests()
