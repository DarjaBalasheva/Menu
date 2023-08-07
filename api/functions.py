def int_to_str(obj):
    if isinstance(obj, int):
        return str(obj)
    raise TypeError(f"Object of type '{type(obj).__name__}' is not JSON serializable")
