import os


def package_root():
    return os.path.join(os.path.dirname(__file__))


def get_schema_file(name):
    root = package_root()
    return os.path.join(root, "schemas", "{}.yaml".format(name))


def convert_path(path):
    """Convert to the path the server will accept.

    Args:
        path (str): Local file path.
            e.g.:
                "D:/work/render/19183793/max/d/Work/c05/112132P-embery.jpg"

    Returns:
        str: Path to the server.
            e.g.:
                "/D/work/render/19183793/max/d/Work/c05/112132P-embery.jpg"

    """
    lower_path = path.replace('\\', '/')
    if lower_path[1] == ":":
        path_lower = lower_path.replace(":", "")
        path_server = "/" + path_lower
    else:
        path_server = lower_path[1:]

    return path_server


def ensure_paths(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
