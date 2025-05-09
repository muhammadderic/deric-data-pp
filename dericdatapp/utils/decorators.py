import inspect
import functools
import io
from contextlib import redirect_stdout

def add_raw_support(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    def raw(pure=False):
        source = inspect.getsource(func)
        if pure:
            # Simple regex/logic to strip comments for the 'pure' requirement
            import re
            # Remove docstrings (lines between triple quotes)
            source = re.sub(r'["\']{3}.*?["\']{3}', '', source, flags=re.DOTALL)
            # Remove single line comments
            source = "\n".join([line for line in source.splitlines() if not line.strip().startswith("#")])
        
        print(source)

    wrapper.raw = raw
    return wrapper


class PromptResult:
    def __init__(self, func, args, kwargs, header=None, footer=None):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.header = header
        self.footer = footer

        self._executed = False
        self._captured_output = None

    def _execute_and_capture(self):
        """Run function once and capture its printed output."""
        if not self._executed:
            buffer = io.StringIO()
            with redirect_stdout(buffer):
                self.func(*self.args, **self.kwargs)

            self._captured_output = buffer.getvalue()
            self._executed = True

    def run(self):
        """Default behavior: print only the function output."""
        self._execute_and_capture()
        print(self._captured_output, end="")

    def prompt(self):
        """Print header + captured output + footer (no re-execution)."""
        self._execute_and_capture()

        if self.header:
            print(self.header.rstrip())

        print(self._captured_output, end="")

        if self.footer:
            print(self.footer.rstrip())

    def __repr__(self):
        # Auto-run when user just calls the function
        self.run()
        return ""

    __str__ = __repr__


def custom_prompt(header=None, footer=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return PromptResult(
                func=func,
                args=args,
                kwargs=kwargs,
                header=header() if callable(header) else header,
                footer=footer() if callable(footer) else footer,
            )
        return wrapper
    return decorator