import re
import sys
import os.path
from pathlib import Path
import ast

empty_line_number = 0  # Counter for empty line


def s001(line):
    """Check for line's length"""
    return len(line) > 79


def s002(line):
    """Check for right indention length"""
    match = re.match(' *', line)
    return len(match.group()) % 4 != 0


def s003(line):
    """Check for unnecessary semicolon"""
    return ';' in re.findall(r'\'.*;.*\'|"\'.*;.*\"|;|#.*;', line)


def s004(line: str) -> bool:
    """Check for at least two spaces required before inline comments"""
    all_hashes = re.findall(r'. *#', line)
    if all_hashes:
        match = re.search(r'[^ ] {0,1}#', all_hashes[0])
        return bool(match)
    return False


def s005(line: str):
    """Check for to do in comment"""
    match = re.search(r'#.*todo', line, flags=re.I)
    return bool(match)


def s006(line):
    """Check for more than two blank lines used before this line"""
    if line and empty_line_number > 2:
        return True


def s007(line):
    """Check for too many spaces after (def or class)"""
    return re.search(r'class {2,}|def {2,}', line)


def s008(line):
    """Check for class name is in CamelCase"""
    if 'class' in line:
        return not re.search(r'class +[A-Z][A-Za-z]+(\(|:)', line)
    return False


def s009(line):
    """Check for function name is in snake_case"""
    if 'def' in line:
        return not re.search(r'def +[a-z_][a-z_\d]+\(', line)
    return False


def s010(tree):
    """Check whether the argumet's name is written in shake_case"""
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.args:
                if not re.match(r'[a-z_\d][a-z_]*$', arg.arg):
                    result.append((node.lineno, arg.arg))
                    break
    return result


def s011(tree):
    """Check whether the variable's name is written in snake_case"""
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for child_node in node.body:
                if isinstance(child_node, ast.Assign):
                    try:
                        if not re.match(r'[a-z_\d][a-z_]+$', child_node.targets[0].attr):  # For class attributes
                            result.append((child_node.lineno, child_node.targets[0].attr))
                    except AttributeError:
                        if not re.match(r'[a-z_\d][a-z_]+$', child_node.targets[0].id):  # For usual variables
                            result.append((child_node.lineno, child_node.targets[0].id))
    return result


def s012(tree):
    """Check whether the argument's default value is immutable"""
    result = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            for arg in node.args.defaults:
                if not any([isinstance(arg, obj) for obj in (ast.Constant, ast.Tuple, ast.Call)]):
                    result.append(arg.lineno)
                    break
    return result


def empty_line_counter(line):
    """Counts empty line"""
    global empty_line_number
    if line.strip() == '':
        empty_line_number += 1
    else:
        empty_line_number = 0


def pep8_checker(file_path):
    """Check file for matching pep8"""
    global empty_line_number
    result = []
    with open(file_path, 'r') as file:
        for i, line in enumerate(file):
            if s001(line):
                result.append(f'{file_path}: Line {i + 1}: S001 Too long')
            if s002(line):
                result.append(f'{file_path}: Line {i + 1}: S002 Indentation is not a multiple of four')
            if s003(line):
                result.append(f'{file_path}: Line {i + 1}: S003 Unnecessary semicolon')
            if s004(line):
                result.append(f'{file_path}: Line {i + 1}: S004 At least two spaces required before inline comments')
            if s005(line):
                result.append(f'{file_path}: Line {i + 1}: S005 TODO found')
            if s006(line):
                result.append(f'{file_path}: Line {i + 1}: S006 More than two blank lines used before this line')
            if s007(line):
                result.append(f'{file_path}: Line {i + 1}: S007 Too many spaces after (def or class)')
            if s008(line):
                result.append(f'{file_path}: Line {i + 1}: S008 Class name class_name should be written in CamelCase')
            if s009(line):
                result.append(f'{file_path}: Line {i + 1}: S009 ' +
                              'Function name function_name should be written in snake_case')
            empty_line_counter(line)

    with open(file_path, 'r') as file_:  # For checking with module 'ast'
        code = file_.read()
        tree = ast.parse(code)
        res_s010 = s010(tree)
        for i in res_s010:
            result.append(f'{file_path}: Line {i[0]}: S010 ' +
                          f'Argument name \'{i[1]}\' should be snake_case')
        res_s011 = s011(tree)
        for i in res_s011:
            result.append(f'{file_path}: Line {i[0]}: S011 ' +
                          f'Variable \'{i[1]}\' in function should be snake_case')
        res_s012 = s012(tree)
        for i in res_s012:
            result.append(f'{file_path}: Line {i}: S012 Default argument value is mutable')

    empty_line_number = 0
    return result


if __name__ == '__main__':
    path = sys.argv[1]
    if '.' in path:     # if path is file
        for i in pep8_checker(os.path.normpath(path)):
            print(i)
    else:               # if path is directory
        files = list(Path(path).glob('**/*.py'))  # all files from all inner directory
        for f in files:
            for i in pep8_checker(os.path.normpath(f)):
                print(i)
