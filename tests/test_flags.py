import unittest

from luster.flags import BaseFlags


class Example(BaseFlags):
    foo = 1 << 0
    bar = 1 << 1
    baz = 1 << 2


class TestInternalHelpers(unittest.TestCase):
    def test_flags(self) -> None:
        assert Example.foo == (1 << 0)
        assert Example.bar == (1 << 1)

        flags = Example(foo=True, baz=False)

        assert flags.value == (Example.foo)
        assert flags.foo
        assert not flags.baz
        assert not flags.bar

        flags.bar = True
        assert flags.bar
        assert flags.value == (Example.foo | Example.bar)


if __name__ == "__main__":
    unittest.main()
