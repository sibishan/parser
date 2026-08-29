"""
only checking for lexical validility 
"""

from lexer import Lexer
from lexer import Numeral, Variable, Space, Glyph, Symbol

TOKEN_TYPES = (Numeral, Variable, Space, Glyph, Symbol)

def test(case, expected):
    mine = Lexer.tokenise(case)
    assert mine == expected, (
        f"FAILED {case!r}: GOT: {mine}, EXPECTED: {expected}"
    )

test("", [])
# test(94, []) # LEXER: Input is NOT a string! should be raised
# test("😀", []) # LEXER: '😀' is ILLEGAL character should be raised

test("   ", [Space(3)])
test("a" + " " * 100 + "b", [Variable('a'), Space(100), Variable('b')])
# test("\t", []) # LEXER: '\t' is ILLEGAL character should be raised
# test("\n", []) # LEXER: '\n' is ILLEGAL character should be raised
# test("a\tb", []) # LEXER: '\t' is ILLEGAL character should be raised
# test("\u00a0", []) # LEXER: '\xa0' is ILLEGAL character should be raised
# test("\u3000", []) # LEXER: '\u3000' is ILLEGAL character should be raised

# glyphs
test("++", [Glyph.ADD, Glyph.ADD])
test("+×∸", [Glyph.ADD, Glyph.MUL, Glyph.SUB])
test("1+2", [Numeral('1'), Glyph.ADD, Numeral('2')])
test("x→y", [Variable('x'), Glyph.RIGHT, Variable('y')])
test("∸5", [Glyph.SUB, Numeral('5')])
test("+×∸⊤⊥←↑→↓∷Θ", [Glyph.ADD, Glyph.MUL, Glyph.SUB, Glyph.TRUE, Glyph.FALSE, Glyph.LEFT, Glyph.UP, Glyph.RIGHT, Glyph.DOWN, Glyph.DEF, Glyph.THETA])

# symbols
test(")(", [Symbol.RIGHT_BRACKET, Symbol.LEFT_BRACKET])
test(")", [Symbol.RIGHT_BRACKET])
test("(", [Symbol.LEFT_BRACKET])
test("λ", [Symbol.LAMBDA])
test(".", [Symbol.DOT])
test("λ.", [Symbol.LAMBDA, Symbol.DOT])
test("λλ", [Symbol.LAMBDA, Symbol.LAMBDA])
test("λ.x", [Symbol.LAMBDA, Symbol.DOT, Variable('x')])
test("x.y", [Variable('x'), Symbol.DOT, Variable('y')])
test("( )", [Symbol.LEFT_BRACKET, Space(1), Symbol.RIGHT_BRACKET])
test("...", [Symbol.DOT, Symbol.DOT, Symbol.DOT])
test("λ1.1", [Symbol.LAMBDA, Numeral('1'), Symbol.DOT, Numeral('1')])

# numerals
test("0123456789", [Numeral('0123456789')])
test("9" * 200, [Numeral("9" * 200)]) 
test("  67 ", [Space(2), Numeral('67'), Space(1)])
test("6.9", [Numeral('6'), Symbol.DOT, Numeral('9')])
test(".5", [Symbol.DOT, Numeral('5')])
test("1. ", [Numeral('1'), Symbol.DOT, Space(1)])
test("2..3", [Numeral('2'), Symbol.DOT, Symbol.DOT, Numeral('3')])
test(" 2a", [Space(1), Numeral('2'), Variable('a')])
test("007", [Numeral("007")])
test("λ 3  ", [Symbol.LAMBDA, Space(1), Numeral('3'), Space(2)])

# variables
test(" sibi69 ", [Space(1), Variable("sibi69"), Space(1)])
test(" realm-heart ", [Space(1), Variable("realm-heart"), Space(1)])
test("a2b", [Variable("a2b")])
test("9tera", [Numeral('9'), Variable("tera")])
test("1a2", [Numeral('1'), Variable('a2')])
test("a1b2c", [Variable('a1b2c')])
test("(abc)", [Symbol('('), Variable('abc'), Symbol(')')])
# test("a;", []) # LEXER: ';' is ILLEGAL character should be raised
# test("@", []) # LEXER: '@' is ILLEGAL character should be raised

# abstractions
test("λ sibi . xxx ", [Symbol.LAMBDA, Space(1), Variable("sibi"), Space(1), Symbol.DOT, Space(1), Variable("xxx"), Space(1)])
test("λx.λy.x", [Symbol.LAMBDA, Variable('x'), Symbol.DOT, Symbol.LAMBDA, Variable('y'), Symbol.DOT, Variable('x')])
test("λ  x  .  x", [
    Symbol.LAMBDA, Space(2), Variable('x'), Space(2), Symbol.DOT, Space(2), Variable('x'),
])
test("λrealm-heart.realm-heart", [
    Symbol.LAMBDA, Variable('realm-heart'), Symbol.DOT, Variable('realm-heart'),
])

# applications
test("()", [Symbol.LEFT_BRACKET, Symbol.RIGHT_BRACKET])
test("((", [Symbol.LEFT_BRACKET, Symbol.LEFT_BRACKET])
test("( sibi xxx ) ", [Symbol.LEFT_BRACKET, Space(1), Variable("sibi"), Space(1), Variable("xxx"), Space(1), Symbol.RIGHT_BRACKET, Space(1)])
test("(λx.x  y)", [Symbol.LEFT_BRACKET, Symbol.LAMBDA, Variable("x"), Symbol.DOT, Variable("x"), Space(2), Variable("y"), Symbol.RIGHT_BRACKET])
test("(λ(x.x) y)", [Symbol.LEFT_BRACKET, Symbol.LAMBDA, Symbol.LEFT_BRACKET, Variable("x"), Symbol.DOT, Variable("x"), Symbol.RIGHT_BRACKET, Space(1), Variable("y"), Symbol.RIGHT_BRACKET])
test("(λx.x)(λy.y)", [
    Symbol.LEFT_BRACKET, Symbol.LAMBDA, Variable('x'), Symbol.DOT, Variable('x'), Symbol.RIGHT_BRACKET,
    Symbol.LEFT_BRACKET, Symbol.LAMBDA, Variable('y'), Symbol.DOT, Variable('y'), Symbol.RIGHT_BRACKET,
])
test("(" * 50 + "x" + ")" * 50,
     [Symbol.LEFT_BRACKET] * 50 + [Variable('x')] + [Symbol.RIGHT_BRACKET] * 50)
test("(λx.x+1)", [
    Symbol.LEFT_BRACKET, Symbol.LAMBDA, Variable('x'), Symbol.DOT,
    Variable('x'), Glyph.ADD, Numeral('1'), Symbol.RIGHT_BRACKET,
])
test("(x→y ∷ z)", [
    Symbol.LEFT_BRACKET, Variable('x'), Glyph.RIGHT, Variable('y'), Space(1),
    Glyph.DEF, Space(1), Variable('z'), Symbol.RIGHT_BRACKET,
])


# hyphens
test("a-", [Variable('a-')])
test("a--b", [Variable('a--b')])
test("a-1", [Variable('a-1')])
# test("-a", []) # LEXER: Variable can NOT start with - should be raised       
# test("1-", []) # LEXER: Variable can NOT start with - should be raised

test("6.9", [Numeral('9'), Symbol.DOT, Numeral('6')]) # FAILED '6.9': GOT: [Numeral(value='6'), <Symbol.DOT: '.'>, Numeral(value='9')], EXPECTED: [Numeral(value='9'), <Symbol.DOT: '.'>, Numeral(value='6')]

print("all tests passed")