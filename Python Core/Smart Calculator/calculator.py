import re


def assign_var(exp):
    key, val = re.findall('[A-Za-z]+|[+-]?[0-9]+', exp)
    if val.isalpha():
        variables[key] = variables.get(val, False)
    else:
        variables[key] = int(val)


def checker(exp: str) -> str:
    def is_valid_var(var):
        return bool(re.match('^[A-Za-z]+$', var))

    def is_valid_val(val):
        return bool(re.match('^[+-]?[0-9]+$', val))

    def check_scope(expression):
        stack = []
        for i in expression:
            if i == '(':
                stack.append(i)
            if i == ')':
                if not stack:
                    return False
                stack.pop()
        if not stack:
            return True
        return False

    def check_operators(expression):
        for i in expression:
            if not re.match(r'^[A-Za-z]+$|^[()]$|^[+-]+$|^[\d]+$|^[*/^]$', i):
                return False
        return True

    exp = exp.strip()
    parsed_exp = [op_simplifier(i) for i in re.findall(r'[+-/*^]+|[()]|[\d]+|[A-Za-z]+', exp)]
    if '=' in exp:
        tokens = re.findall('=|[A-Za-z0-9]+', exp)
        if len(tokens) != 3:
            return 'Invalid assignment'
        if is_valid_var(tokens[0]):
            if is_valid_val(tokens[2]):
                return 'add'
            if is_valid_var(tokens[2]):
                if tokens[2] in variables:
                    return 'add'
                return 'Unknown variable'
            return 'Invalid assignment'
        return 'Invalid identifier'
    if exp.startswith('/'):
        if exp in ('/help', '/exit'):
            return exp
        return 'Unknown command'
    if is_valid_val(exp):
        return exp
    if len(parsed_exp) == 1:
        if is_valid_var(exp):
            if exp in variables:
                return 'show value'
            return 'Unknown variable'
        return 'Invalid identifier'
    if check_scope(parsed_exp) and check_operators(parsed_exp):
        return 'calculate'
    return 'Invalid expression'


def get_precedence(operator: str) -> int:
    if operator in '+-':
        return 1
    if operator in '*/':
        return 2
    if operator == '^':
        return 3
    return 0


def op_simplifier(operator: str) -> str:
    if re.match('^[+-]+$', operator):
        return '+' if operator.count("-") % 2 == 0 else '-'
    return operator


def to_postfix(exp: 'valid expression str') -> 'postfix expression list':
    res_exp, stack = [], []
    parsed_exp = [op_simplifier(i) for i in re.findall(r'[+-/*^]+|[()]|[\d]+|[A-Za-z]+', exp)]
    for i in parsed_exp:
        if i.isalnum():
            res_exp.append(i)
        elif not stack or get_precedence(stack[-1]) < get_precedence(i) or i == '(' or stack[-1] == '(':
            stack.append(i)
        elif i == ')':
            top_item = None
            while top_item != '(':
                top_item = stack.pop()
                if top_item != '(':
                    res_exp.append(top_item)
        else:
            while not (not stack or get_precedence(stack[-1]) < get_precedence(i)):
                res_exp.append(stack.pop())
            stack.append(i)
    while not (not stack or get_precedence(stack[-1]) < get_precedence(i)):
        res_exp.append(stack.pop())
    return res_exp


def replace_vars(exp: list) -> list:
    for i in range(len(exp)):
        if re.match('^[A-Za-z]+$', exp[i]):
            exp[i] = str(variables.get(exp[i], exp[i]))
    return exp


def calculate(exp):
    postfix_exp = replace_vars(to_postfix(exp))
    while len(postfix_exp) != 1:
        for i in range(len(postfix_exp) - 2):
            if re.match(r'^-?[\d]*$', postfix_exp[i]) and re.match(r'^-?[\d]*$', postfix_exp[i + 1]) \
                    and postfix_exp[i + 2] in '+-*/^':
                first = postfix_exp.pop(i)
                second = postfix_exp.pop(i)
                operator = postfix_exp.pop(i)
                if operator == '^':
                    operator = '**'
                elif operator == '/':
                    operator = '//'
                postfix_exp.insert(i, str(eval(first + operator + second)))
                break
    return postfix_exp[0]


variables = {}
while True:
    inp = input().strip()
    if inp == '':
        continue
    command = checker(inp)
    match command:
        case '/exit':
            print('Bye!')
            break
        case '/help':
            print('The program calculates the sum of numbers')
        case 'add':
            assign_var(inp)
        case 'show value':
            print(variables[inp])
        case 'calculate':
            print(calculate(inp))
        case _:
            print(command)