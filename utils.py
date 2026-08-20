def is_glyph(s):
    if s in [
        '+', '×', '∸', '⊤', '⊥', '←', '↑', '→', '↓', '∷', 'Θ'
    ]:
        return True

    return False

def is_symbol(s):
    if s in [
        '(', ')', 'λ', '.'
    ]:
        return True

    return False

def classify(s):
    if s.isdigit():
        return "DIGIT"
    elif 'a' <= s <= 'z':
        return "LETTER"
    elif s.isspace():
        return "SPACE"
    elif is_glyph(s):
        return "GLYPH"
    elif is_symbol(s):
        return "SYMBOL"
    elif s == ";":
        return None
    else:
        raise TypeError(f"LEXER: {s} can NOT be classified")
    