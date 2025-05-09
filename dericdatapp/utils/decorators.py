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
    def __init__(self, func, args, kwargs, header, footer):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self.header = header
        self.footer = footer

    def prompt(self):
        """Executes the function framed by the modular header and footer."""
        # 1. Print the long-form Header from your .txt file
        if self.header:
            print(self.header.strip())
            print()
        
        # 2. Execute the actual function (which prints its own tables/text)
        result = self.func(*self.args, **self.kwargs)
        
        # 3. Print the Footer
        if self.footer:
            print()
            print(self.footer.strip())
            
        return result

    def __repr__(self):
        return "<dericdatapp.PromptResult: Call .prompt() to view analysis>"

def custom_prompt(header=None, footer=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # We return the OBJECT without running the function yet
            # This allows the .prompt() call to control the timing
            return PromptResult(func, args, kwargs, header, footer)
        return wrapper
    return decorator