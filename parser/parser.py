from ast_nodes.ast_nodes import NumberNode, BinOpNode


class Parser:

    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0


    def current_token(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None


    def eat(self):
        self.pos += 1


    def parse(self):
        return self.expr()


    # handles + and -
    def expr(self):

        node = self.term()

        while self.current_token() and self.current_token()[0] in ("PLUS", "MINUS"):
            operator = self.current_token()[1]
            self.eat()

            right = self.term()
            node = BinOpNode(node, operator, right)

        return node


    # handles * and /
    def term(self):

        node = self.factor()

        while self.current_token() and self.current_token()[0] in ("MULTIPLY", "DIVIDE"):
            operator = self.current_token()[1]
            self.eat()

            right = self.factor()
            node = BinOpNode(node, operator, right)

        return node


    # handles numbers
    def factor(self):

        token = self.current_token()

        if token[0] == "NUMBER":
            self.eat()
            return NumberNode(token[1])