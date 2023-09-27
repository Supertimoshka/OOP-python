class Parser:

    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    priority_of_operations = {'(': 0, ')': 0, '+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    
    def __init__(self, expression):
        self.expression = ''.join(expression.split())
        
    def get_tokens(self):
        token = ''
        tokens = []
        operations = Parser.priority_of_operations.keys()

        if self.expression[0] in operations and self.expression[0] != '(' or self.expression[-1] in operations and self.expression[-1] != ')':
            raise ValueError('Missing operand')
        
        for i in range(0, len(self.expression)):
            if self.expression[i] in Parser.numbers:
                try:
                    if tokens[-1] == ')':
                        raise ValueError('Missing operation')
                except IndexError:
                    pass
                token += self.expression[i]
            elif self.expression[i] == '.':
                token += self.expression[i]
            elif self.expression[i] in operations:
                if token != '':
                    if self.expression[i] == '(':
                        raise ValueError('Missing operation')
                    try:
                        float(token)
                    except ValueError:
                        raise ValueError('Wrong number')
                    tokens.append(token)
                try:
                    if tokens[-1] in operations:
                        if tokens[-1] == '(' and self.expression[i] != '(':
                            raise ValueError('Missing operand')
                        elif tokens[-1] == ')' and self.expression[i] == '(':
                            raise ValueError('Missing operation')
                        elif tokens[-1] != '(' and tokens[-1] != ')' and self.expression[i] != '(':
                            raise ValueError('Missing operand')
                except IndexError:
                    pass
                tokens.append(self.expression[i])
                token = ''
            elif self.expression[i] != '.':
                raise ValueError(f'Incorrect symbol \'{self.expression[i]}\'')
        if token != '':        
            tokens.append(token)

        return tokens


class Calculator:

    def convert_to_postfix_notation(tokens):
        stack = []
        output = []
        for token in tokens:
            if token not in Parser.priority_of_operations.keys():
                output.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                if len(stack) == 0:
                    raise ValueError('Missing opening parenthesis')
                else:
                    try:
                        while stack[-1] != '(':
                            output.append(stack.pop())
                        else:
                            stack.pop()
                    except IndexError:
                        raise ValueError('Missing opening parenthesis')
            else:
                try:
                    while Parser.priority_of_operations[stack[-1]] >= Parser.priority_of_operations[token]:
                        output.append(stack.pop())
                    else:
                        stack.append(token)
                except IndexError:
                    stack.append(token)
        else:
            while len(stack) > 0:
                if stack[-1] == '(':
                    raise ValueError('Missing closing parenthesis')
                output.append(stack.pop())
        return output

    def try_to_calculate(tokens_in_postfix_notation):
        stack = []
        while len(tokens_in_postfix_notation) > 0:
            if tokens_in_postfix_notation[0] not in Parser.priority_of_operations.keys():
                stack.append(tokens_in_postfix_notation.pop(0))
            else:
                match tokens_in_postfix_notation[0]:
                    case '+':
                        stack.append(float(stack.pop(-2)) + float(stack.pop(-1)))
                    case '-':
                        stack.append(float(stack.pop(-2)) - float(stack.pop(-1)))
                    case '*':
                        stack.append(float(stack.pop(-2)) * float(stack.pop(-1)))
                    case '/':
                        if float(stack[-1]) == 0:
                            raise ValueError('Division by zero')
                        stack.append(float(stack.pop(-2)) / float(stack.pop(-1)))
                    case '^':
                        stack.append(float(stack.pop(-2)) ** float(stack.pop(-1)))
                tokens_in_postfix_notation.pop(0)
        return stack[0]

    def calculate(self, expression):
        if expression == '':
            raise ValueError('Empty expression')
        parser = Parser(expression)
        tokens = parser.get_tokens()
        tokens_in_postfix_notation = Calculator.convert_to_postfix_notation(tokens)
        print(tokens_in_postfix_notation)
        value = Calculator.try_to_calculate(tokens_in_postfix_notation)
        if value % 1 != 0:
            return value
        else:
            return int(value)
    
c = Calculator()
print(c.calculate(". + 1"))