"""Text formatting utilities for console output."""


class TableFormatter:
    """Turns rows of data into an aligned plain-text table (a utility class)."""

    MAX_CELL_WIDTH = 28

    @staticmethod
    def heading(title):
        """Return a title underlined with '=' characters."""
        return f"{title}\n{'=' * len(title)}"

    @classmethod
    def _clip(cls, value):
        text = "" if value is None else str(value)
        text = text.replace("\n", " ")
        if len(text) <= cls.MAX_CELL_WIDTH:
            return text
        return text[: cls.MAX_CELL_WIDTH - 3] + "..."

    @classmethod
    def render(cls, headers, rows):
        """Return a table string, or a friendly message when there are no rows."""
        if not rows:
            return "(no records found)"
        clipped = [[cls._clip(cell) for cell in row] for row in rows]
        widths = []
        for index, header in enumerate(headers):
            column_width = max(len(row[index]) for row in clipped)
            widths.append(max(len(str(header)), column_width))

        def line(cells):
            return " | ".join(str(cell).ljust(widths[i]) for i, cell in enumerate(cells))

        separator = "-+-".join("-" * width for width in widths)
        output = [line(headers), separator]
        output.extend(line(row) for row in clipped)
        return "\n".join(output)
