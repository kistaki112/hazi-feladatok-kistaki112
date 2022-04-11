import json
import sys
import unittest

from threading import Thread
import functools


def test():
    print("Paste the JSON document of test data, then trigger an <<EOF>> (CTRL+Z in Windows, CTRL+D in PyCharm)")
    test_suite = json.load(sys.stdin)
    ProgTest().run_tests(test_suite, sys.modules["__main__"])


class ProgTest(unittest.TestCase):

    @staticmethod
    def timeout(limit):
        def deco(func):
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                res = [Exception("time limit [%s seconds] exceeded" % (limit))]

                def new_func():
                    try:
                        res[0] = func(*args, **kwargs)
                    except Exception as e:
                        res[0] = e

                t = Thread(target=new_func, daemon=True)
                try:
                    t.start()
                    t.join(limit)
                except Exception as je:
                    print("error starting thread")
                    raise je
                ret = res[0]
                if isinstance(ret, BaseException):
                    raise ret
                return ret
            
            return wrapper

        return deco

    def run_tests(self, test_suite, solution):
        final_result = []

        for function_name in test_suite:
            print(f"\n=== TEST function {function_name}() ===")

            total = len(test_suite[function_name])
            passed = 0

            try:
                function = getattr(solution, function_name)
            except AttributeError:
                print("Missing function")
                final_result.append((function_name, 0, total))
                continue

            for test_case in test_suite[function_name]:
                print(f"\n>> {', '.join(str(p) for p in test_case['in'])}")
                try:
                    test_function = self.timeout(limit=test_case["limit"])(function)
                    result = test_function(*test_case["in"])
                    self.assertEqual(result, test_case["out"])
                    print(f"<< {result}")
                    print("status: OK")
                    passed += 1
                except AssertionError as e:
                    print(f"{e}")
                except Exception as e:
                    print(f"status: ERROR:\n{e}")

            final_result.append((function_name, passed, total))

        print("\n=== FINAL RESULTS ===")
        for result in final_result:
            print(
                f"\tfunction {result[0]}(): {result[1]} / {result[2]} => {round(result[1] / float(result[2]) * 100, 2)}%")
