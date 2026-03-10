from ast_nodes.ast_nodes import NumberNode, BinOpNode

class Interpreter:

    def visit(self, node):

        if isinstance(node, NumberNode):
            return node.value

        if isinstance(node, BinOpNode):

            left = self.visit(node.left)
            right = self.visit(node.right)

            if node.operator == "+":
                return left + right

            if node.operator == "-":
                return left - right

            if node.operator == "*":
                return left * right

            if node.operator == "/":
                return left / right