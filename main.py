import sys

from parser import Parser, print_tree


VALID = 0
INVALID = 1


def main(argv: list[str]) -> int:
    args = argv[1:]

    verbose = False
    if args and args[0] in ("-v", "--verbose"):
        verbose = True
        args = args[1:]

    if len(args) != 1:
        print(
            f"usage: python3 {argv[0]} [-v] \"<input>\"",
            file=sys.stderr
        )
        return INVALID

    try:
        result = Parser.parse(args[0], verbose)

    except ValueError as error:
        print(error, file=sys.stderr)
        return INVALID

    except TypeError as error:
        print(error, file=sys.stderr)
        return INVALID

    except RecursionError:
        print("PARSER: Input nested too deeply", file=sys.stderr)
        return INVALID

    if verbose:
        code, tree = result
        print_tree(tree)
        return code

    return result


if __name__ == "__main__":
    sys.exit(main(sys.argv))