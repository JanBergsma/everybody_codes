import re
from collections.abc import Callable, Sequence
from copy import deepcopy
from typing import Any

from termcolor import colored

TestDict = dict[str, Any]
AssertFunction = Callable[[Any, Any], bool]


def test(
    *args: Any,
    tests: Sequence[TestDict] | None = None,
    assert_funct: AssertFunction = lambda x, y: x == y,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Decorator to run parameterized tests using run_tests_params.

    keyword argument:
        tests: Sequence[Sequence[Any]] = [{
            "name": "test",
            "diagram": "###A###",
            "expected": "A"}
        ],
        assert_funct: AssertFunction = lambda x, y: x == y

    Returns:
        A decorator that runs the tests.

    Example:
        >>> @test(tests=[{"name": "test", "diagram": "###A###", "expected": "A"}])
        ... def dummy(diagram):
        ...     return diagram[3]
        test test passed, for dummy.
        Success
    """

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        if tests is not None:
            run_tests_params(func, tests, assert_funct)
        return func

    return decorator


def run_tests(
    f: Callable[..., Any],
    tests: Sequence[Sequence[Any]],
    assert_funct: AssertFunction = lambda x, y: x == y,
) -> None:
    """
    Run a series of tests on a function.

    Args:
        f: Function to test.
        tests: Sequence of test cases, each a sequence where the last element is expected output.
        assert_funct: Function to compare actual and expected output.

    Example:
        >>> def add(a, b): return a + b
        >>> run_tests(add, [["sum", 2, 3, 5], ["zero", 0, 0, 0]])
        test sum passed, for add.
        test zero passed, for add.

        Success
    """

    def test(*args: Any) -> None:
        expected: Any = args[-1]
        actual: Any = f(*args[:-1])
        if not assert_funct(actual, expected):
            raise AssertionError(f"{actual} should be {expected}")

    no_errors: bool = True
    for _args in deepcopy(tests):
        name: str = ""
        try:
            name, *_args = _args
            test(*_args)
            print(colored(f"test {name} passed, for {f.__name__}.", "green"))
        except Exception as e:
            print(
                colored(f"test {name} failed! ***{e.args}, for {f.__name__}.", "red")
            )  # noqa
            no_errors = False

    print()
    if no_errors:
        print(colored("Success", "green"))
    else:
        print(colored("***Errors", "red"))


def test_all_solutions(
    test_harnass: Callable[[Callable[..., Any]], Callable[..., Any]],
    obj: Any,
    pattern: str,
    tests: Sequence[Sequence[Any]],
    assert_funct: AssertFunction = lambda x, y: x == y,
) -> None:
    found: bool = False
    for method in (e for e in dir(obj) if re.match(pattern, e)):
        run_tests(test_harnass(getattr(obj(), method)), tests, assert_funct)
        found = True
        print("\n" * 2)

    if found:
        print(colored("All matched methodes have been tested.", "green"))
    else:
        print(
            colored(
                "***There was no method, that did match the pattern!", "red"
            )  # noqa
        )  # noqa


def run_tests_params(
    f: Callable[..., Any],
    tests: Sequence[TestDict],
    assert_funct: AssertFunction = lambda x, y: x == y,
) -> None:
    def _test(test: TestDict) -> bool:
        name, *params, expected = test.items()
        _, name_val = name
        _, expected_val = expected
        params_dict: dict[str, Any] = dict(params)
        actual: Any = f(**params_dict)
        if assert_funct(actual, expected_val):
            print(colored(f"Test {name_val} passed, for {f.__name__}.", "green"))
            return True
        print(
            colored(
                f"Test {name_val }: {actual} should be {expected_val}, for {f.__name__}.",  # noqa
                "red",
            )
        )
        return False

    print()
    all_passed: bool = True
    for test in deepcopy(tests):
        all_passed &= _test(test)

    if all_passed:
        print(colored("Success", "green"))
    else:
        print(colored("***Errors", "red"))


def test_all_solutions_params(
    test_harnass: Callable[[Callable[..., Any]], Callable[..., Any]],
    obj: Any,
    tests: Sequence[TestDict],
    pattern: str = r"^[^_+]",
    assert_funct: AssertFunction = lambda x, y: x == y,
) -> None:
    found: bool = False
    for method_name in (e for e in dir(obj()) if re.match(pattern, e)):
        method: Callable[..., Any] = getattr(obj(), method_name)

        run_tests_params(test_harnass(method), tests, assert_funct)
        found = True
        print("\n" * 2)

    if found:
        print(colored("All matched methodes have been tested.", "blue"))
    else:
        print(colored("***There was no method, that did match the pattern!", "red"))


def standard_test_harnass(f: Callable[..., Any]) -> Callable[..., Any]:
    def func(**kwarg: Any) -> Any:
        actual: Any = f(**kwarg)
        return actual

    func.__name__ = f.__name__
    return func
