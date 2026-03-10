from lexer.lexer import tokenize
from parser.parser import Parser
from interpreter.interpreter import Interpreter

with open("tests/test_program.txt") as f:
    code = f.read()

tokens = tokenize(code)

print("Tokens:", tokens)

parser = Parser(tokens)
tree = parser.parse()

print("AST:", tree)

interpreter = Interpreter()
result = interpreter.visit(tree)

print("Result:", result)