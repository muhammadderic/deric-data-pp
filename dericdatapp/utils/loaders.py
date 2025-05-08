from pathlib import Path

def load_template(filename: str) -> str:
    """
    Locates and reads a text file from the templates directory.
    
    Args:
        filename (str): The name of the file (e.g., 'numerical_expert.txt')
        
    Returns:
        str: The raw content of the file with formatting preserved.
    """
    # 1. Get the path of the current file (loaders.py)
    # 2. Go up two levels to reach the project root
    # 3. Enter the 'templates' folder
    base_path = Path(__file__).resolve().parent.parent
    template_path = base_path / "templates" / filename
    
    try:
        with open(template_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return f"[Error] Template '{filename}' not found at {template_path}"