import unittest

from utils.formatters import TableFormatter


class TableFormatterTests(unittest.TestCase):
    def test_heading_underlines_title(self):
        self.assertEqual(TableFormatter.heading("Menu"), "Menu\n====")

    def test_render_empty_rows(self):
        self.assertEqual(TableFormatter.render(("A", "B"), []), "(no records found)")

    def test_render_aligns_columns(self):
        table = TableFormatter.render(("ID", "Name"), [(1, "Tendai"), (22, "Rudo")])
        lines = table.split("\n")
        self.assertEqual(len(lines), 4)
        self.assertTrue(lines[0].startswith("ID"))
        self.assertIn("Tendai", lines[2])
        self.assertEqual(len(lines[2]), len(lines[3]))

    def test_render_clips_long_cells(self):
        table = TableFormatter.render(("Text",), [("x" * 100,)])
        self.assertIn("...", table)
        self.assertLessEqual(max(len(line) for line in table.split("\n")), 28)


if __name__ == "__main__":
    unittest.main()
