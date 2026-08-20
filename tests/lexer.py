from lexer import LexicalAnalyser
from lexer import Numeral, Variable, Space, Glyph, Symbol

def test(case, actual):
    mine = LexicalAnalyser.tokenise(case)
    assert mine == actual, (
        f"FAILED {case!r}: GOT: {mine}, EXPECTED: {actual}"
    )

# numeral
test("  67 ", [Space(2), Numeral('67'), Space(1)])
test("6.9", [Numeral('6'), Symbol('.'), Numeral('9')])
test(".5", [Symbol('.'), Numeral('5')])
test("1. ", [Numeral('1'), Symbol('.'), Space(1)])
test("2..3", [Numeral('2'), Symbol('.'), Symbol('.'), Numeral('3')])
test(" 2a", [Space(1), Numeral('2'), Variable('a')])
test("λ 3  ", [Symbol('λ'), Space(1), Numeral('3'), Space(2)])

# # variable
# print(LexicalAnalyser.tokenise(" sibi69 "))
# print(LexicalAnalyser.tokenise(" realm-heart "))

# # abstraction
# print(LexicalAnalyser.tokenise("λ sibi . xxx "))

# # application
# print(LexicalAnalyser.tokenise("( sibi xxx ) "))