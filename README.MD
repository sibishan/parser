# LL(1) Parser

## Grammar

The grammar is given in EBNF. `{ ... }` means zero or more repetitions, `|` means alternation, and
quoted items are literal characters.

```ebnf
input       = { " " } , expression , { " " } ;

expression  = numeral | variable | glyph | abstraction | application ;

numeral     = digit , { digit } ;
digit       = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;

variable    = letter , { letter | digit | "-" } ;
letter      = "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j"
            | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t"
            | "u" | "v" | "w" | "x" | "y" | "z" ;

glyph       = "+" | "×" | "∸" | "⊤" | "⊥" | "←" | "↑" | "→" | "↓" | "∷" | "Θ" ;

abstraction = "λ" , { " " } , variable , { " " } , "." , { " " } , expression ;

application = "(" , { " " } , expression , " " , { " " } , expression , { " " } , ")" ;
```


### Glyph reference

| Glyph | Name    | Glyph | Name  | Glyph | Name  |
| :---: | ------- | :---: | ----- | :---: | ----- |
|  `+`  | ADD     |  `⊥`  | FALSE |  `↓`  | DOWN  |
|  `×`  | MUL     |  `←`  | LEFT  |  `∷`  | DEF   |
|  `∸`  | SUB     |  `↑`  | UP    |  `Θ`  | THETA |
|  `⊤`  | TRUE    |  `→`  | RIGHT |       |       |

---

## Usage

Requires **Python 3.12+** (the code uses `enum.StrEnum` and PEP 604 unions). No dependency installations are needed.

```console
$ python3 main.py "<input>"
$ python3 main.py -v "<input>"      # to print the parse tree
```

Here, `<input>` is the string to be parsed. Surround it with quotation marks so that
spaces and shell metacharacters such as `(`, `)` and `*` are passed through intact.

The parser does not expect an end-of-string marker, so do not append `⊣` to the input.

### Exit codes

| Code | Meaning                                                     |
| ---- | ----------------------------------------------------------- |
| `0`  | valid — the input is a sentence of the grammar               |
| `1`  | invalid — a lexical or syntactic error, or bad CLI arguments |

Nothing is written to stdout on success unless `-v` is given; error messages go to stderr. This makes
the program easy to drive from a script:

```console
$ python3 main.py "λx.x"
$ echo $?
0
```

Errors are prefixed with the stage that raised them, `LEXER:` or `PARSER:`:

```console
$ python3 main.py "x_y"
LEXER: '_' is ILLEGAL character
$ python3 main.py "λ1.x"
PARSER: Expected a variable, got '1'
```

### Use as a library

```python
from parser import Parser, print_tree

code = Parser.parse("(x y)")                       # -> 0
code, tree = Parser.parse("(x y)", verbose=True)   # verbose: (0, ParseNode(...))
print_tree(tree)
```

### Running the tests

```console
$ python3 -m tests.lexer
$ python3 -m tests.parser
```

---

## File structure

```
parser/
├── main.py            CLI entry point: argument handling, exit codes, error reporting
├── parser.py          recursive-descent parser, grammar in the module docstring, parse tree + printer
├── lexer.py           character-level scanner: string -> list of tokens
├── tokens.py          token types (Numeral, Variable, Space) and enums (Glyph, Symbol)
├── tests/
│   ├── parser.py      end-to-end validity tests driven through main()
│   └── lexer.py       tokenisation tests
├── LICENSE            MIT
└── README.md
```

---

## Examples

A valid input:

```console
$ python3 main.py "((+ 1) 2)"
$ echo $?
0
```

The same input with `-v`, which prints the parse tree:

```console
$ python3 main.py -v "((+ 1) 2)"
└── Expression
    └── Application
        ├── (
        ├── Expression
        │   └── Application
        │       ├── (
        │       ├── Expression
        │       │   └── Glyph
        │       │       └── +
        │       ├── Expression
        │       │   └── Numeral
        │       │       └── 1
        │       └── )
        ├── Expression
        │   └── Numeral
        │       └── 2
        └── )
```

An invalid input, with the diagnostic on stderr:

```console
$ python3 main.py "(x y"
PARSER: Expected ')' to close an application, got end of input
$ echo $?
1
```

---

## License

MIT — see [LICENSE](LICENSE).