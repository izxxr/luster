import unittest

from luster.permissions import PermissionOverwrite, Permissions


class TestPermissionOverwrites(unittest.TestCase):
    def test_pairs(self) -> None:
        po = PermissionOverwrite(
            send_messages=False,
            speak=False,
            connect=True,
            view_channels=True,
        )
        allow = Permissions(connect=True, view_channels=True)
        deny = Permissions(send_messages=True, speak=True)

        assert po.pair() == (allow, deny)
        assert PermissionOverwrite.from_pair(allow, deny) == po


if __name__ == "__main__":
    unittest.main()
