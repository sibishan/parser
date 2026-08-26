from parser import Parser, print_tree

code, tree = Parser.parse("((x y) z)", versbose=True)
print(print_tree(tree))