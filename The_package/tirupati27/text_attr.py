attr_doc="""
--------------------------------------
HOW TO GIVE THE VALUE OF `attr`
        or
SOME EXAMPLES OF USING TEXT ATTRIBUTES
--------------------------------------
Text styles:
    bold       - Bold text
    italic     - Italic text
    underline  - Underlined text
    strikethrough - strike text
    blink      - blink text (not supported by some terminal)
    inverse    - inverse (not supported by some terminal)

Foreground colors:
    <color-name>   - Any color defined in your JSON database
    <r;g;b>        - RGB color code e.g. 255;0;200
    rand_color     - Pick a random color from the JSON database

Background colors:
    bg:<color-name>    - Background with a specific color
    bg:<r;g;b>         - RGB color code e.g. 255;0;200
    bg:rand_color      - Random background color

EXAMPLES:
    "red"
    "red+underline"
    "bg: red + rand_color"
    "bold + italic + 255;0;100"
    "strikethrough + bg: rand_color"
    "255;100;40 + bg: 80;100;255 + italic"
    etc...
This is how you can use any combination of text attributes
"""
__doc__=f"""
====================================
    Terminal Text Styling Utility
====================================
1. IMPORT AND USE
-----------------
    The 'text_attr' module provides following objects:

    (i) build_ansi_escape_code()
    (ii) p_text()
    (iii) pprint()
    (iv) attr_doc (variable which contains usage doc)
    (iv) COLORS (A dict, which can be extended with more colors)

    from text_attr import build_ansi_escape_code
    from text_attr import p_text
    from text_attr import pprint
    from text_attr import attr_doc
    import text_attr
    text_attr.COLORS["teal"] = "0;128;128"  # extend with more colors

2. RUN FROM TERMINAL
-----------------
    python text_attr.py --attr "red+bold" --sep "-" --end "\\n" text to style
{attr_doc}"""

import os, sys, random
from .validate_rgb import validate_rgb

# --- YOU CAN ADD MORE COLORS HERE TO USE ---
COLORS = {
    "black": "0;0;0",      "white": "255;255;255", "red": "255;0;0",
    "green": "0;255;0",    "blue": "0;0;255",      "yellow": "255;255;0",
    "cyan": "0;255;255",   "magenta": "255;0;255", "gray": "128;128;128",
    "orange": "255;165;0", "purple": "128;0;128",  "pink": "255;192;203",
    "brown": "165;42;42"
}
_C_VALUES = tuple(COLORS.values())
_STYLES = {
    "bold": "1",
    "italic": "3",
    "underline": "4",
    "blink": "5",
    "inverse": "7",
    "strikethrough": "9",
}

def build_ansi_escape_code(attr: str) -> str:
    """
Build ANSI escape codes string for given attributes.
Returns:
        - Numeric part of ANSI code (\\033['__THIS-PART__'m): if user passed a meaningful attr.
        - empty string: if user passed meaningless attr."""
    codes = set()
    fg = "38;2;{}"
    bg = "48;2;{}"
    for a in attr.replace(" ", "").lower().split("+"):
        if a in _STYLES:
            codes.add(_STYLES[a])
        elif a == "rand_color":
            codes.add(fg.format(random.choice(_C_VALUES)))
        elif a == "bg:rand_color":
            codes.add(bg.format(random.choice(_C_VALUES)))
        # seeking for 'bg:255;20;50' or 'bg:red'
        elif a.startswith("bg:"):
            c = a[3:]
            if c in COLORS:
                codes.add(bg.format(COLORS[c]))
            else:
                c = validate_rgb(c)
                if c:
                    codes.add(bg.format(c))
        # seeking for '255;20;50' or 'green'
        else:
            if a in COLORS:
                codes.add(fg.format(COLORS[a]))
            else:
                a = validate_rgb(a)
                if a:
                    codes.add(fg.format(a))
    return ";".join(codes) if codes else ""

def p_text(text: str, attr: str)-> str:
    '''
    p_text == pretty text
    A wrapper of 'build_ansi_escape_code' for decorated text output

    returns:
        - ansi decorated text for terminal output if supplied attr is correct,
        - otherwise returns the text as it is
    '''
    ansi_code = build_ansi_escape_code(attr)
    if ansi_code:
        text = f"\033[{ansi_code}m{text}\033[0m"
    return text

def pprint(*args, attr: str,
           sep: str = ' ', end: str = '\n',
           file=None, flush: bool = False) -> None:
    """Print with ANSI styles/colors"""
    if file is None:
        file = sys.stdout
    text = sep.join(map(str, args))
    if not attr or os.getenv("NO_COLOR"):
        print(text, end=end, file=file, flush=flush)
    else:
        print(p_text(text, attr), end=end, file=file, flush=flush)

def main():
    import argparse
    p = argparse.ArgumentParser(description="Terminal Text Styling Utility")
    p.add_argument("--attr", help="e.g. red+bold | bg:blue+white | rand_color+underline")
    p.add_argument("--sep", default="-", help="Value of `sep` argument in `print()` function")
    p.add_argument("--end", default="\n", help="Value of `end` argument in `print()` function")
    p.add_argument("--usage", action="store_true", help="Show usage information")
    args, remaining = p.parse_known_args()
    if args.usage:
        print(__doc__)
        sys.exit(0)
    if not remaining:
        p.error("at least one text argument is required")
        sys.exit(1)
    pprint(*remaining, attr=args.attr, sep=args.sep, end=args.end)


if __name__ == "__main__":
    main()
