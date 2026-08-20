from lexer import LexicalAnalyser

print(LexicalAnalyser.tokenise("  67 "))
print(LexicalAnalyser.tokenise(" sibi69 "))
print(LexicalAnalyser.tokenise(" realm-heart "))
print(LexicalAnalyser.tokenise("λ sibi . xxx "))
print(LexicalAnalyser.tokenise("( sibi xxx ) "))