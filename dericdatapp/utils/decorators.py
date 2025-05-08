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
    def __init__(self, data, header, footer):
        self.data = data
        self.header = header
        self.footer = footer

    def prompt(self):
        """Prints the framed result and returns the data."""
        # Python's print() will render the triple-quoted string perfectly
        print(self.header) 
        print(self.data)
        print(self.footer)
        return self.data

    def __repr__(self):
        # This ensures that if they DON'T call .prompt(), it just looks like normal data
        return repr(self.data)

def custom_prompt(header="--- START ---", footer="--- END ---"):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Run the function logic
            result_data = func(*args, **kwargs)
            # Return the object that has the .prompt() method
            return PromptResult(result_data, header, footer)
        return wrapper
    return decorator