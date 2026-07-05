import unittest
from pathlib import Path

from auto_reload import get_cog_files


class AutoReloadTests(unittest.TestCase):
    def test_get_cog_files_skips_non_python_and_init(self):
        root = Path(__file__).resolve().parent.parent
        cogs_dir = root / "cogs"
        files = get_cog_files(cogs_dir)

        self.assertIn("decorate.py", files)
        self.assertNotIn("__init__.py", files)
        self.assertTrue(all(name.endswith(".py") for name in files))


if __name__ == "__main__":
    unittest.main()
