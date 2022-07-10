import unittest

from luster.internal import helpers


class TestInternalHelpers(unittest.TestCase):
    def test_handle_optional_field(self) -> None:
        data = {
            "id": 1234,
            "none": None,
        }

        assert helpers.handle_optional_field(data, "id") == data["id"]
        assert helpers.handle_optional_field(data, "non_existing") == None
        assert helpers.handle_optional_field(data, "non_existing", False) == False
        assert helpers.handle_optional_field(data, "none", False, None) == False


if __name__ == "__main__":
    unittest.main()
