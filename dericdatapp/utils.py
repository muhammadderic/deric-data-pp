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