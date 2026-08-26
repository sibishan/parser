from dataclasses import dataclass
from enum import StrEnum

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