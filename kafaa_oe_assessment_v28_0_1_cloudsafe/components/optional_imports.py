
def optional_import(name):
    try:
        module = __import__(name)
        return module
    except Exception:
        return None
