from importlib import import_module
from pathlib import Path


def get_modules_from_import(package):
    """Returns all modules within the given imported package.

    Args:
        package (module): The package containing error modules.

    Returns:
        dict: A dictionary mapping module names (without the .py extension)
              to their imported modules.
    """

    imported_modules = []
    path = Path(package.__path__[0])

    for file in path.iterdir():
        if (
            file.is_file()
            and file.suffix == ".py"
            and not file.name.startswith("__")
        ):
            module_name = file.name.replace(".py", "")
            import_path = f"{package.__name__}.{module_name}"
            imported_modules.append(import_module(import_path))

    return imported_modules
