import re

# Define token types
TOKEN_TYPES = [
    ("NUMBER", r'\d+'),
    ("PLUS", r'\+'),
    ("MINUS", r'-'),
    ("MULTIPLY", r'\*'),
    ("DIVIDE", r'/'),
    ("LPAREN", r'\('),
    ("RPAREN", r'\)'),
    ("WHITESPACE", r'\s+'),
]

def tokenize(code):
    tokens = []
    
    while code:
        match = None
        
        for token_type, pattern in TOKEN_TYPES:
            regex = re.compile(pattern)
            match = regex.match(code)
            
            if match:
                value = match.group(0)
                
                if token_type != "WHITESPACE":
                    tokens.append((token_type, value))
                
                code = code[len(value):]
                break
        
        if not match:
            raise SyntaxError("Invalid character: " + code[0])
    
    return tokens