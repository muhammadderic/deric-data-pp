import importlib.resources as pkg_resources

def load_template(filename: str) -> str:
    return pkg_resources.files("dericdatapp.templates") \
        .joinpath(filename) \
        .read_text(encoding="utf-8")

def get_prompt(name: str):
    return lambda: load_template(f"{name}.txt")