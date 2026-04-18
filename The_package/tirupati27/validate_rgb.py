def validate_rgb(rgb: str, sep: str = ";")-> str:
    """validate string RGB codes like '255;40;100;'
    Returns the formatted rgb string if validation is true, otherwise empty string.
    """
    try:
        rgb_parts = [i for i in rgb.replace(" ", "").split(sep) if i]
        if len(rgb_parts) == 3 and all(0 <= int(i) < 256 for i in rgb_parts):
            return sep.join(rgb_parts)
    except:
        pass
    return ""