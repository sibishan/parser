from tokens import Numeral, Variable, Space, Glyph, Symbol

Token = Numeral | Variable | Space | Glyph | Symbol

GLYPHS  = {g.value for g in Glyph}
SYMBOLS = {y.value for y in Symbol}

class Lexer:
    @staticmethod
    def tokenise(s: str) -> list[Token]:
        if not isinstance(s, str):
            raise TypeError("LEXER: Input is NOT a string")

        tokens = []
        n = len(s)
        i = 0
        while i < n:
            char = s[i]
            if char in GLYPHS:
                tokens.append(Glyph(char))
                i += 1

            elif char in SYMBOLS:
                tokens.append(Symbol(char))
                i += 1

            elif char == " ":
                j = i
                while j < n and s[j] == " ":
                    j += 1
                tokens.append(Space(j - i))
                i = j

            elif "0" <= char <= "9":
                j = i
                while j < n and ("0" <= s[j] <= "9"):
                    j += 1
                tokens.append(Numeral(s[i:j]))
                i = j

            elif "a" <= char <= "z":
                j = i
                while j < n and ("a" <= s[j] <= "z" or "0" <= s[j] <= "9" or s[j] == "-"):
                    j += 1
                tokens.append(Variable(s[i:j]))
                i = j

            elif char == "-":
                raise ValueError(f"LEXER: Variable can NOT start with -")

            else:
                raise ValueError(f"LEXER: {char!r} is ILLEGAL character")

        return tokens
