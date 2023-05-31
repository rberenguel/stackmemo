def colorify(txt):
    opened = None
    space = True  # Start of string
    new_text = []
    mapping = {"_": "#003399 ", "*": "#009933 ", "`": "#993300 "}
    for c in txt:
        if c in mapping:
            if not opened and space:
                # Initial opening
                opened = c
                new_text.append(mapping[c])
            else:
                if opened == c:
                    # Closing a know opening
                    new_text.append("# ")
                    opened = None
                else:
                    # Symbol in the middle, ignore
                    new_text.append(c)
                space = False
        elif c == " ":
            space = True
            if opened:
                new_text.append("# ")
                new_text.append(c)
                new_text.append(mapping[opened])
            else:
                new_text.append(c)
        elif c == "\n":
            # Newline?, which is like an space after all
            space = True
            new_text.append(c)
        else:
            space = False
            new_text.append(c)
    return "".join(new_text).replace("  ", " ")
