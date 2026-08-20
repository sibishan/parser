from dataclasses import dataclass
from enum import StrEnum

from utils import classify, is_glyph

@dataclass(frozen=True)
class Numeral:
    value : str

    def __str__(self):
        return self.value

@dataclass(frozen=True)
class Variable:
    value : str

    def __str__(self):
        return self.value

@dataclass(frozen=True)
class Space:
    size : int

    def __str__(self):
        return self.size

class Glyph(StrEnum):
    ADD = '+'
    MUL = '×'
    SUB = '∸'
    TRUE = '⊤'
    FALSE = '⊥'
    LEFT = '←'
    UP = '↑'
    RIGHT = '→'
    DOWN = '↓'
    DEF = '∷'
    THETA = 'Θ'

class Symbol(StrEnum):
    LEFT_BRACKET = '('
    RIGHT_BRACKET = ')'
    LAMBDA = 'λ'
    DOT = '.'

Token = Numeral | Variable | Space | Glyph | Symbol

class LexicalAnalyser:
    def tokenise(s):
        tokens = []
        buffer = ""
        cur = None

        if not isinstance(s, str):
            raise TypeError("LEXER: Input is NOT a string!")
        s += ";"

        idx = 0
        while idx < len(s) - 1:
            cur = classify(s[idx])
            nex = classify(s[idx + 1])

            if cur == "GLYPH":
                tokens.append(Glyph(f'{s[idx]}'))
            elif cur == "SYMBOL":
                if s[idx] == "(":
                    tokens.append(Symbol("("))
                elif s[idx] == ")":
                    tokens.append(Symbol(")"))
                elif s[idx] == "λ":
                    tokens.append(Symbol("λ"))
                elif s[idx] == ".":
                    tokens.append(Symbol("."))
                else:
                    raise TypeError(f"LEXER: {s[idx]} is an issue")
            elif cur == nex or (cur == "LETTER" and nex == "DIGIT"):
                buffer += s[idx]
            elif not cur == "SPACE":
                if cur == "DIGIT":
                    buffer += s[idx]
                    tokens.append(Numeral(buffer))
                    buffer = ""
                elif cur == "LETTER":
                    buffer += s[idx]
                    tokens.append(Variable(buffer))
                    buffer = ""
            elif cur == "SPACE" and not nex == "SPACE":
                buffer += s[idx]
                tokens.append(Space(len(buffer)))
                buffer = ""
            else:
                raise TypeError(f"LEXER: {s[idx]} is an issue")

            idx += 1

        return tokens
            
