from contextlib import redirect_stderr
from io import StringIO

from main import main


def test(case, expected):
    with redirect_stderr(StringIO()):
        code = main(["main.py", case])

    assert code == expected, (
        f"FAILED {case!r}: GOT: {code}, EXPECTED: {expected}"
    )

    print(f"ok  {case!r} -> {code}")

test("(sibi  r)", 0)
test("(sibi  r)", 0)

