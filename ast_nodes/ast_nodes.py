class NumberNode:
    def __init__(self, value):
        self.value = int(value)

    def __repr__(self):
        return f"Number({self.value})"


class BinOpNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def __repr__(self):
        return f"({self.left} {self.operator} {self.right})"