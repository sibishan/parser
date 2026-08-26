from dataclasses import dataclass
from typing import Union, Tuple

from tokens import Numeral, Variable, Space, Glyph, Symbol
from lexer import Lexer

"""
GRAMMAR
input = { " " } , expression , { " " } ;

expression = numeral | variable | glyph | abstraction | application ;

numeral = digit , { digit } ;
digit = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

variable = letter , { letter | digit | "-" } ;
letter = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"
       | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t"
       | "u" | "v" | "w" | "x" | "y" | "z" ;

glyph = "+" | "×" | "∸" | "⊤" | "⊥" | "←" | "↑" | "→" | "↓" | "∷" | "Θ" ;

abstraction = "λ" , { " " } , variable , { " " } , "." ,  { " " } ,expression ;

application = "(" , { " " } , expression , " ", { " " } , expression , { " " } , ")" ;
"""

Token = Numeral | Variable | Space | Glyph | Symbol

@dataclass(frozen=True)
class ParseNode:
    name: str
    children: list

@dataclass(frozen=True)
class Leaf:
    value: str

class Parser:

    @staticmethod
    def parse(s: str, versbose=False) -> Union[int, Tuple[int, ParseNode]]:
        tokens = Lexer.tokenise(s)
        i = 0

        # helpers
        def current() -> Token | None:
            if i >= len(tokens):
                return None
            return tokens[i]

        def consume() -> Token:
            nonlocal i

            if i >= len(tokens):
                raise ValueError("PARSER: Unexpected end of input")

            token = tokens[i]
            i += 1
            return token

        def describe(token: Token | None) -> str:
            if token is None:
                return "end of input"
            if isinstance(token, Space):
                return f"{token.size} space(s)"
            return repr(str(token))

        def expect(symbol: Symbol, where: str) -> Token:
            if current() != symbol:
                raise ValueError(
                    f"PARSER: Expected {symbol.value!r} {where}, "
                    f"got {describe(current())}"
                )
            return consume()

        def skip_space() -> None:
            if isinstance(current(), Space):
                consume()

        def expect_space(where: str) -> None:
            if not isinstance(current(), Space):
                raise ValueError(
                    f"PARSER: Expected a space {where}, "
                    f"got {describe(current())}"
                )
            consume()

        # grammar rules

        # input = { " " } , expression , { " " }
        def input() -> ParseNode:

            skip_space()

            tree = expression()

            skip_space()

            if i != len(tokens):
                raise ValueError(
                    f"PARSER: Unexpected token "
                    f"{describe(current())} after expression"
                )

            if versbose:
                return 0, tree
            else:
                return 0

        # expression = numeral | variable | glyph | abstraction | application
        def expression() -> ParseNode:

            token = current()

            if isinstance(token, Numeral):
                child = numeral()

            elif isinstance(token, Variable):
                child = variable()

            elif isinstance(token, Glyph):
                child = glyph()

            elif token == Symbol.LAMBDA:
                child = abstraction()

            elif token == Symbol.LEFT_BRACKET:
                child = application()

            else:
                raise ValueError(
                    f"PARSER: Expected an expression, "
                    f"got {describe(token)}"
                )

            return ParseNode(
                "Expression",
                [child]
            )

        # numeral = digit , { digit }
        def numeral() -> ParseNode:

            token = consume()

            return ParseNode(
                "Numeral",
                [Leaf(token.value)]
            )

        # variable = letter , { letter | digit | "-" }
        def variable() -> ParseNode:

            token = current()

            if not isinstance(token, Variable):
                raise ValueError(
                    f"PARSER: Expected a variable, "
                    f"got {describe(token)}"
                )

            consume()

            return ParseNode(
                "Variable",
                [Leaf(token.value)]
            )

        # glyph = "+" | "×" | "∸" | "⊤" | "⊥" | "←" | "↑" | "→" | "↓" | "∷" | "Θ"
        def glyph() -> ParseNode:

            token = consume()

            return ParseNode(
                "Glyph",
                [Leaf(token.value)]
            )

        # abstraction = "λ" , { " " } , variable , { " " } , "." , { " " } , expression
        def abstraction() -> ParseNode:

            children = []

            expect(Symbol.LAMBDA, "to start an abstraction")
            children.append(Leaf(Symbol.LAMBDA.value))

            skip_space()

            children.append(variable())

            skip_space()

            expect(Symbol.DOT, "after the bound variable")
            children.append(Leaf(Symbol.DOT.value))

            skip_space()

            children.append(expression())

            return ParseNode(
                "Abstraction",
                children
            )

        # application = "(" , { " " } , expression , " " , { " " } , expression , { " " } , ")"
        def application() -> ParseNode:

            children = []

            expect(Symbol.LEFT_BRACKET, "to start an application")
            children.append(Leaf(Symbol.LEFT_BRACKET.value))

            skip_space()

            children.append(expression())

            # This separator is required, not optional.
            expect_space("between the two expressions")

            children.append(expression())

            skip_space()

            expect(Symbol.RIGHT_BRACKET, "to close an application")
            children.append(Leaf(Symbol.RIGHT_BRACKET.value))

            return ParseNode(
                "Application",
                children
            )

        return input()

# utils
def print_tree(node, prefix="", is_last=True):

    connector = "└── " if is_last else "├── "

    if isinstance(node, Leaf):
        print(prefix + connector + node.value)
        return

    if isinstance(node, ParseNode):

        print(prefix + connector + node.name)

        child_prefix = prefix + (
            "    " if is_last else "│   "
        )

        for i, child in enumerate(node.children):
            print_tree(
                child,
                child_prefix,
                i == len(node.children) - 1
            )