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
    """
    Holds execution context and allows re-running with prompt.
    """

    def __init__(self, func, args, kwargs, header=None, footer=None):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.header = header
        self.footer = footer

    def prompt(self):
        if self.header:
            print(self.header.rstrip())

        # Re-run function (side-effect print)
        self.func(*self.args, **self.kwargs)

        if self.footer:
            print(self.footer.rstrip())

    # Prevent notebook from printing None / object
    def __repr__(self):
        return ""

    __str__ = __repr__


def custom_prompt(header=None, footer=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Default behavior → execute immediately
            func(*args, **kwargs)

            return PromptResult(
                func=func,
                args=args,
                kwargs=kwargs,
                header=header() if callable(header) else header,
                footer=footer() if callable(footer) else footer,
            )
        return wrapper
    return decorator