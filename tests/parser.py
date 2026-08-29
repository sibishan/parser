from contextlib import redirect_stderr
from io import StringIO

from main import main, VALID, INVALID


def test(case, expected):
    buf = StringIO()
    with redirect_stderr(buf):
        code = main(["main.py", case])
    assert code == expected, (
        f"FAILED {case!r}: GOT: {code}, EXPECTED: {expected}\n"
        f"stderr:\n{buf.getvalue()}"
    )
    print(f"ok  {case!r} -> {code}")


LETTERS = set("abcdefghijklmnopqrstuvwxyz")
DIGITS = set("0123456789")
GLYPHS = ["+","×","∸","⊤","⊥","←","↑","→","↓","∷","Θ"]

# ---------------------------------------------------------------------------
# 1. every kind of expression in every position where an expression may appear
# ---------------------------------------------------------------------------
KINDS = {
    "numeral": "1",
    "variable": "x",
    "glyph": "+",
    "abstraction": "λx.x",
    "application": "(x y)",
}
for kind, e in KINDS.items():
    test(e, VALID)                                          # alone
    test(f"  {e}  ", VALID)                                 # with top-level padding
    test(f"λv.{e}", VALID)                                  # as an abstraction body
    test(f"({e} z)", VALID)                                 # first operand of an application
    test(f"(z {e})", VALID)                                 # second operand
    test(f"({e} {e})", VALID)                               # both operands
    test(f"λ{e}.x", VALID if kind == "variable" else INVALID)   # only a variable can be bound
    test(f"{e} {e}", INVALID)                                # two expressions at top level
    test(f"({e})", INVALID)                                  # one expression in appilcation
    test(f"({e} {e} {e})", INVALID)                          # three expressions in appilcation

# ---------------------------------------------------------------------------
# 2. numeral = digit , { digit }
# ---------------------------------------------------------------------------
for d in "0123456789":
    test(d, VALID)
test("42", VALID)
test("1234567890", VALID)
test("007", VALID)           # leading zeros: nothing in the grammar forbids them
test("0000", VALID)
test("1.5", INVALID)         # no decimal point
test("1,000", INVALID)
test("1_000", INVALID)
test("-1", INVALID)          # no sign
test("+1", INVALID)          # '+' is a glyph, then a numeral
test("1+", INVALID)
test("1e5", INVALID)
test("0x1f", INVALID)
test("1-", INVALID)          # numeral, then - but a variable can't start with - (lexer lvl fail)
test("1-2", INVALID)
test("1x", INVALID)          # numeral, then a variable
test("1 2", INVALID)         # two numerals seperated by space at top level

# ---------------------------------------------------------------------------
# 3. variable = letter , { letter | digit | "-" }
# ---------------------------------------------------------------------------
for l in "abcdefghijklmnopqrstuvwxyz":
    test(l, VALID)
test("xyz", VALID)
test("sibi", VALID)
test("x1", VALID)
test("x123", VALID)
test("a1b2c3", VALID)
test("x-", VALID)           # a trailing '-' is legal
test("x--", VALID)
test("x-y", VALID)
test("x-1", VALID)
test("x1-", VALID)
test("x-y-z", VALID)
test("x-1-y-2", VALID)
test("lambda", VALID)       # there are no reserved words
test("if", VALID)
test("true", VALID)         # not a boolean, is a variable
test("false", VALID)
test("v", VALID)            
test("x", VALID)            
test("X", INVALID)           # upper case is not a letter
test("Abc", INVALID)
test("aBc", INVALID)
test("abC", INVALID)
test("-", INVALID)           # '-' cannot start a variable ...
test("-x", INVALID)
test("--", INVALID)
test("_", INVALID)           # ... and '_' is not in the alphabet at all
test("_x", INVALID)
test("x_", INVALID)
test("x_y", INVALID)
test("x.y", INVALID)
test("x'", INVALID)
test("x y", INVALID)
test("xλ", INVALID)          # variable, then lamda
test("x+", INVALID)
test("x×", INVALID)

# ---------------------------------------------------------------------------
# 4. glyph = "+" | "×" | "∸" | "⊤" | "⊥" | "←" | "↑" | "→" | "↓" | "∷" | "Θ"
# ---------------------------------------------------------------------------
for g in GLYPHS:
    test(g, VALID)
    test(f" {g} ", VALID)
    test(f"({g} x)", VALID)
    test(f"(x {g})", VALID)
    test(f"({g} {g})", VALID)
    test(f"λx.{g}", VALID)
    test(g + g, INVALID)          # glyph followed by junk
    test(f"{g} {g}", INVALID)     # two expressions at top level
    test(f"({g}{g})", INVALID)    # application needs a space between operands
    test(f"λ{g}.x", INVALID)      # a glyph is not a variable
    test(g + "x", INVALID)
    test(g + "1", INVALID)
# NOT glyphs (different code point, or ASCII art)
for s in ["*", "-", "−",            # '×' / '∸' stand-ins  (− is U+2212 minus)
          "÷", "·", "⋅", "∙", "∓", "⨪",
          "T", "F", "⟙", "⟘", "⟂", "⊢", "⊣", "|",   # '⊤' / '⊥' stand-ins
          "^", "<-", "->", "⇐", "⇑", "⇒", "⇓", "↔", "↕", "⟵", "⟶", "➔", "⇧",  # arrows
          "::", ":", "∶", "⁚",       # '∷' stand-ins (∶ is U+2236 ratio)
          "θ", "ϴ", "Ө", "ϑ", "Ɵ", "O", "0O",   # 'Θ' stand-ins (ϴ U+03F4, Ө Cyrillic U+04E8)
          "＋", "✕", "⨯", "=", "≡"]:
    test(s, INVALID)

# ---------------------------------------------------------------------------
# 5. abstraction = "λ" , { " " } , variable , { " " } , "." , { " " } , expression
# ---------------------------------------------------------------------------
test("λx.x", VALID)
test("λx.y", VALID)
test("λx.1", VALID)
test("λx.+", VALID)
test("λx.(x y)", VALID)
test("λx.λy.x", VALID)
test("λx.λy.λz.((x z) (y z))", VALID)   # S combinator
test("λx.(x x)", VALID)
test("λ x . x", VALID)                  # spaces allowed after λ, around '.'
test("λ  x  .  x", VALID)
test("λ x.x", VALID)
test("λx .x", VALID)
test("λx. x", VALID)
test("λx-y.x-y", VALID)                 # bound variable may contain '-' and digits
test("λx1.x1", VALID)
test("λx-.x", VALID)
test("λxyz.xyz", VALID)                 # bound variable may be more than one letter
test("λlambda.lambda", VALID)
test("λx.x-", VALID)                    # body is the variable 'x-'
test("λx.xy", VALID)                    # body is the variable 'xy', NOT 'x' applied to 'y'
test("λx.x1", VALID)
test("λx.λx.x", VALID)                  # shadowing is semantic; syntactically fine
test("λ", INVALID)
test("λ ", INVALID)
test("λ.", INVALID)
test("λ.x", INVALID)                     # missing bound variable
test("λ .x", INVALID)
test("λx", INVALID)                      # missing '.' and body
test("λ x", INVALID)
test("λx ", INVALID)
test("λx.", INVALID)                     # missing body
test("λx. ", INVALID)
test("λx..x", INVALID)
test("λx.x.", INVALID)
test("λx.x.x", INVALID)
test("λx x", INVALID)                    # missing '.'
test("λxx", INVALID)                     # that's the variable 'xx' with no '.'
test("λx,x", INVALID)
test("λx:x", INVALID)
test("λx→x", INVALID)
test("λ1.x", INVALID)                    # bound variable must be a variable, not a numeral ...
test("λ12.x", INVALID)
test("λ+.x", INVALID)                    # ... nor a glyph ...
test("λ(x).x", INVALID)                  # ... nor an application
test("λ(x y).x", INVALID)
test("λλx.x", INVALID)
test("λX.x", INVALID)
test("λx.X", INVALID)
test("λ-x.x", INVALID)
test("λx.-", INVALID)
test("λx.1x", INVALID)                   # body numeral '1', then junk
test("λx.λy", INVALID)
test("λx.λ", INVALID)
test("λx.λy.", INVALID)
test("λx.(x)", INVALID)
test("λx.x y", INVALID)                  # body is ONE expression; 'y' is trailing junk
test("λx.x λy.y", INVALID)
test("λx.x)", INVALID)
test("(λx.x)", INVALID)                  # parens are ONLY for application: a lone parenthesised
test("((λx.x) y)", INVALID)              #   expression is invalid, however natural it loVALIDs ...
test("(λx.x y)", VALID)                 # ... this is how "apply λx.x to y" is written
test("\\x.x", INVALID)                   # ASCII stand-ins for λ
test("/x.x", INVALID)
test("lambda x.x", INVALID)
test("Λx.x", INVALID)                    # U+039B capital lambda
test("𝜆x.x", INVALID)                    # U+1D706 mathematical italic small lambda (NFKC-folds to λ)
test("𝛌x.x", INVALID)                    # U+1D6CC mathematical bold small lambda
test("ƛx.x", INVALID)                    # U+019B lambda with strVALIDe
test("λx·x", INVALID)                    # dot loVALID-alikes: U+00B7 middle dot
test("λx⋅x", INVALID)                    #   U+22C5 dot operator
test("λx∙x", INVALID)                    #   U+2219 bullet operator
test("λx．x", INVALID)                    #   U+FF0E fullwidth full stop (NFKC-folds to '.')
test("λx。x", INVALID)                    #   U+3002 ideographic full stop
test("λx…x", INVALID)                    #   U+2026 horizontal ellipsis

# ---------------------------------------------------------------------------
# 6. application = "(" , { " " } , expression , " " , { " " } , expression , { " " } , ")"
# ---------------------------------------------------------------------------
test("(x y)", VALID)
test("(sibi r)", VALID)
test("(sibi  r)", VALID)
test("(x  y)", VALID)                   # any number >= 1 of spaces between operands
test("( x y)", VALID)                   # optional spaces after '(' ...
test("(x y )", VALID)                   # ... and before ')'
test("( x y )", VALID)
test("(   x    y    )", VALID)
test("(1 2)", VALID)
test("(x 1)", VALID)
test("(1 x)", VALID)
test("(+ 1)", VALID)
test("(1 +)", VALID)
test("(x x)", VALID)
test("(x-y z-w)", VALID)
test("(x- y)", VALID)
test("(x y-)", VALID)
test("(a1 b2)", VALID)
test("((x y) z)", VALID)
test("(x (y z))", VALID)
test("((x y) (z w))", VALID)
test("(((x y) z) w)", VALID)
test("(x (y (z w)))", VALID)
test("((+ 1) 2)", VALID)                # binary operators are curried prefix, not infix
test("((× 2) 3)", VALID)
test("((∸ x) y)", VALID)
test("(λx.x y)", VALID)
test("(x λy.y)", VALID)
test("(λx.x λy.y)", VALID)
test("(λx.(x x) λx.(x x))", VALID)
test("((λx.x y) z)", VALID)
test("(λf.λx.(f x) g)", VALID)
test("( λx.x y )", VALID)
test("(λ x . x y)", VALID)              # body ends at the first space; that space is the separator
test("(λx.x- y)", VALID)
test("((x y)  z)", VALID)
test("()", INVALID)
test("( )", INVALID)
test("(  )", INVALID)
test("(x)", INVALID)                     # exactly two operands: never one ...
test("( x )", INVALID)
test("(x )", INVALID)
test("( x)", INVALID)
test("(1)", INVALID)
test("(+)", INVALID)
test("((x y))", INVALID)
test("(x y z)", INVALID)                 # ... never three
test("(1 2 3)", INVALID)
test("(x y z w)", INVALID)
test("(x (y z) w)", INVALID)
test("(x y (z w))", INVALID)
test("((x y) z w)", INVALID)
test("(1 + 2)", INVALID)                 # infix is three expressions
test("(x - y)", INVALID)
test("(x → y)", INVALID)
test("(xy)", INVALID)                    # no separator: this is the single variable 'xy'
test("(12)", INVALID)
test("(+×)", INVALID)
test("(x-y)", INVALID)
test("(x -y)", INVALID)                  # '-y' is not an expression
test("(λx.xy)", INVALID)                 # body swallows 'xy'; nothing left for operand two
test("((x y)z)", INVALID)                # separator required even after a ')'
test("(x(y z))", INVALID)
test("(x λy.y", INVALID)
test("(x y", INVALID)                    # unbalanced parentheses
test("(x y ", INVALID)
test("x y)", INVALID)
test("(x", INVALID)
test("(", INVALID)
test(")", INVALID)
test("((", INVALID)
test("))", INVALID)
test("((x y)", INVALID)
test("(x y))", INVALID)
test("((x y) z", INVALID)
test("(x (y z)", INVALID)
test("x (y z))", INVALID)
test("(())", INVALID)
test("(() ())", INVALID)
test("(x ())", INVALID)
test("(() x)", INVALID)
test("(x,y)", INVALID)                   # wrong separators
test("(x, y)", INVALID)
test("(x;y)", INVALID)
test("(x.y)", INVALID)
test("(x\ty)", INVALID)                  # only U+0020 is a space
test("(x\ny)", INVALID)
test("(x\r\ny)", INVALID)
test("(x\u00a0y)", INVALID)              # no-break space
test("(x\u2009y)", INVALID)              # thin space
test("(x\u3000y)", INVALID)              # ideographic space
test("(x\u200by)", INVALID)              # zero-width space
test("[x y]", INVALID)                   # wrong brackets
test("{x y}", INVALID)
test("<x y>", INVALID)
test("⟨x y⟩", INVALID)
test("（x y）", INVALID)                  # fullwidth parens U+FF08/U+FF09 (NFKC-fold to ASCII)
test("(x y）", INVALID)
test("（x y)", INVALID)
test("(x y)(z w)", INVALID)              # two applications side by side
test("(x y) (z w)", INVALID)
test("(x y)z", INVALID)
test("x(y z)", INVALID)
test("x (y z)", INVALID)
test("(x y).", INVALID)

# ---------------------------------------------------------------------------
# 7. input = { " " } , expression , { " " }
# ---------------------------------------------------------------------------
test("", INVALID)                        # empty string: no expression
test(" ", INVALID)
test("     ", INVALID)
test(" x", VALID)
test("x ", VALID)
test(" x ", VALID)
test("   x   ", VALID)
test(" 1 ", VALID)
test(" + ", VALID)
test(" λx.x ", VALID)
test(" (x y) ", VALID)
test("\t", INVALID)                      # only U+0020 counts as a space
test("\n", INVALID)
test("\tx", INVALID)
test("x\t", INVALID)
test("\nx", INVALID)
test("x\n", INVALID)                     # a shell-appended newline must be rejected
test("x\r\n", INVALID)
test("\rx", INVALID)
test(" \tx", INVALID)
test("x \t", INVALID)
test("\u00a0x", INVALID)
test("x\u00a0", INVALID)
test("\u2003x", INVALID)                 # em space
test("\u3000x", INVALID)
test("\u200bx", INVALID)
test("x\u200b", INVALID)
test("\ufeffx", INVALID)                 # UTF-8 byte-order mark
test("\ufeff(x y)", INVALID)
test("x y", INVALID)                     # exactly one expression
test("x  y", INVALID)
test("1 2", INVALID)
test("x 1", INVALID)
test("1 x", INVALID)
test("+ 1", INVALID)
test("+ +", INVALID)
test("λx.x λy.y", INVALID)
test("(x y) z", INVALID)
test("x;", INVALID)                      # stray leading / trailing characters
test(";x", INVALID)
test("x#", INVALID)
test("\"x\"", INVALID)
test("'x'", INVALID)
test("`x`", INVALID)

# ---------------------------------------------------------------------------
# 8. Unicode / UTF-8 traps
# ---------------------------------------------------------------------------
# (a) str.isalpha() is True for every one of these
for s in ["é", "ñ", "ß", "ø", "ç", "α", "ж","х","ª", "ǆ", "ℓ", "𝐱"]:
    test(s, INVALID)
    test("x" + s, INVALID)
    test("λ" + s + ".x", INVALID)
    test("λx." + s, INVALID)
    test("(x " + s + ")", INVALID)
# (b) str.isdigit() / isnumeric() / isdecimal() are True for these
for s in ["١", "٢", "६", "²", "³", "½", "Ⅻ", "⑤", "𝟙", "１"]:
    test(s, INVALID)
    test("1" + s, INVALID)
    test("x" + s, INVALID)
    test("(x " + s + ")", INVALID)
# (c) str.isspace() is True for these
for s in ["\u00a0", "\u2002", "\u2003", "\u2009", "\u202f", "\u3000",
          "\u2028", "\u2029", "\v", "\f"]:
    test(s + "x", INVALID)
    test("x" + s, INVALID)
    test("(x" + s + "y)", INVALID)
    test("λ" + s + "x.x", INVALID)
# (d) NFKC-normalising the input would turn these into VALID strings
test("ｘ", INVALID)                      # fullwidth x
test("ⓧ", INVALID)                       # circled x
test("＋", INVALID)                      # fullwidth plus
test("１", INVALID)                      # fullwidth one
test("ϴ", INVALID)                       # U+03F4 theta symbol -> Θ
test("（x y）", INVALID)
test("𝜆x.x", INVALID)
test("λｘ.x", INVALID)
# (e) combining marks: the base letter is fine, the mark is not
test("x\u0301", INVALID)
test("λ\u0301x.x", INVALID)
test("+\u0301", INVALID)
test("(x y\u0301)", INVALID)
# (f) hyphen look-alikes inside a variable
test("x‐y", INVALID)                     # U+2010 hyphen
test("x‑y", INVALID)                     # U+2011 non-breaking hyphen
test("x–y", INVALID)                     # U+2013 en dash
test("x—y", INVALID)                     # U+2014 em dash
test("x−y", INVALID)                     # U+2212 minus sign
test("x－y", INVALID)                     # U+FF0D fullwidth hyphen-minus
# (g) astral-plane characters (4-byte UTF-8)
test("😀", INVALID)
test("(😀 x)", INVALID)
test("λx.😀", INVALID)
test("x😀", INVALID)

# ---------------------------------------------------------------------------
# 9. composition, nesting depth, input width
# ---------------------------------------------------------------------------
test("λf.λg.λx.(f (g x))", VALID)                     
test("(λn.λf.λx.(f ((n f) x)) λf.λx.x)", VALID)        
test("((+ 1) ((× 2) 3))", VALID)
test("(((Θ λx.x) 1) 2)", VALID)
test("λp.λq.((p q) ⊥)", VALID)
test("((← x) (→ y))", VALID)
test("λ f . λ x . ( f ( f x ) )", VALID)              # maximal spacing everywhere it is allowed
test(" λf.λx.(f (f x)) ", VALID)
test("λf.λx.(f(f x))", INVALID)                       # one missing space

# max depth, just under CPython's default recursion limit of 1000
left = "x"
for _ in range(495):
    left = f"({left} y)"
test(left, VALID)
test(left[:-1], INVALID)                               # one ')' short
test(left + ")", INVALID)                              # one ')' extra
test("(" + left, INVALID)                              # one '(' extra
right = "y"
for _ in range(495):
    right = f"(x {right})"
test(right, VALID)
test(right[:-1], INVALID)
test("λx." * 495 + "x", VALID)
test("λx." * 495, INVALID)
test("λx." * 495 + "x.", INVALID)
mixed = "x"
for _ in range(247):
    mixed = f"λx.({mixed} y)"
test(mixed, VALID)

print("all tests passed")