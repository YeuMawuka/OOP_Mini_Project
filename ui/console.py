"""Console input/output helper."""

from utils.exceptions import ValidationError
from utils.validators import Validators


class Console:
    """Wraps input() and print() so the menus can be tested with scripted input.

    ENCAPSULATION: the input and output functions are private attributes.
    """

    def __init__(self, input_func=input, output_func=print):
        self.__input = input_func
        self.__output = output_func

    def say(self, text=""):
        """Print one line (or block) of text."""
        self.__output(text)

    def read(self, prompt):
        """Read one raw line of input."""
        return self.__input(prompt)

    def ask(self, label, validator=None, current=None, required=True):
        """Ask until the answer is valid.

        `current` is a default that is used when the user just presses Enter; it is
        shown in square brackets. Optional fields (required=False) accept an empty
        answer without running the validator.
        """
        while True:
            hint = f" [{current}]" if current not in (None, "") else ""
            raw = self.read(f"{label}{hint}: ").strip()
            if not raw:
                if current is not None:
                    return current
                if not required:
                    return ""
                self.say(f"  {label} is required.")
                continue
            if validator is None:
                return raw
            try:
                return validator(raw)
            except ValidationError as error:
                self.say(f"  Invalid input: {error}")

    def ask_id(self, label):
        """Ask for a record ID (a positive whole number)."""
        return self.ask(label, lambda value: Validators.positive_int(value, label))

    def ask_choice(self, label, options, current=None):
        """Ask for one value out of a fixed list."""
        full_label = f"{label} ({'/'.join(options)})"
        return self.ask(
            full_label, lambda value: Validators.choice(value, options, label), current
        )

    def confirm(self, question):
        """Ask a yes/no question and return True for yes."""
        while True:
            answer = self.read(f"{question} (y/n): ").strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            self.say("  Please answer y or n.")
