import inspect
import functools

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

    def run(self):
        if not self._executed:
            self.func(*self.args, **self.kwargs)
            self._executed = True

    def prompt(self):
        if self.header:
            print(self.header.rstrip())

        self.run()

        if self.footer:
            print(self.footer.rstrip())

    def __repr__(self):
        # Auto-run for notebook display
        if not self._executed:
            self.run()
        return ""

    __str__ = __repr__


def custom_prompt(header=None, footer=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return PromptResult(
                func,
                args,
                kwargs,
                header() if callable(header) else header,
                footer() if callable(footer) else footer,
            )
        return wrapper
    return decorator