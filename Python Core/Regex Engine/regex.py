def single_char(reg, inp, prev=False):
    """"Check for match single chars"""
    if not reg:
        return True
    if not inp:
        return False
    if reg == '.' and inp and not prev:
        return True
    if reg == inp:
        return True
    return False


def word(reg, inp, index_reg=0, index_inp=0):
    """Check for match"""
    if len(reg) <= index_reg:
        return ''
    if len(inp) <= index_inp:
        if index_reg == len(reg) - 1 and reg[index_reg] in '?*+':
            return ''
        if index_reg == len(reg) - 2 and reg[index_reg + 1] in '?*+':
            return ''
        return False
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    if reg[index_reg] == '\\' and index_reg - 1 >= 0 and reg[index_reg - 1] == '\\':
        if single_char(reg[index_reg], inp[index_inp], prev=True):
            if type(word(reg, inp, index_reg + 1, index_inp + 1)) == bool:
                return False
            return inp[index_inp] + word(reg, inp, index_reg + 1, index_inp + 1)
    if reg[index_reg] == '\\':
        return word(reg, inp, index_reg + 1, index_inp)
    if reg[index_reg] == '.' and index_reg - 1 >= 0 and reg[index_reg - 1] == '\\':
        if single_char(reg[index_reg], inp[index_inp], prev=True):
            if type(word(reg, inp, index_reg + 1, index_inp + 1)) == bool:
                return False
            return inp[index_inp] + word(reg, inp, index_reg + 1, index_inp + 1)
        return word(reg, inp, index_reg + 1, index_inp + 1)
    # \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # ???????????????????????????????????????????????????????????????????
    if reg[index_reg] == '?' and index_reg - 1 >= 0 and reg[index_reg - 1] == '\\':
        if single_char(reg[index_reg], inp[index_inp], prev=True):
            if type(word(reg, inp, index_reg + 1, index_inp + 1)) == bool:
                return False
            return inp[index_inp] + word(reg, inp, index_reg + 1, index_inp + 1)
        return word(reg, inp, index_reg + 1, index_inp + 1)
    if reg[index_reg] == '?':
        return word(reg, inp, index_reg + 1, index_inp)
    if (not single_char(reg[index_reg], inp[index_inp])) and index_reg + 2 < len(reg) and reg[index_reg + 1] == '?':
        return inp[index_inp] + word(reg, inp, index_reg + 3, index_inp+1)
    # ???????????????????????????????????????????????????????????????????
    # *******************************************************************
    if reg[index_reg] == '*':
        if single_char(reg[index_reg - 1], inp[index_inp]):
            return inp[index_inp] + word(reg, inp, index_reg, index_inp + 1)
        return word(reg, inp, index_reg + 1, index_inp)
    if (not single_char(reg[index_reg], inp[index_inp])) and index_reg + 2 < len(reg) and reg[index_reg + 1] == '*':
        return inp[index_inp] + word(reg, inp, index_reg + 3, index_inp+1)
    # *******************************************************************
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if reg[index_reg] == '+' and index_reg - 1 >= 0 and reg[index_reg - 1] == '\\':
        if type(word(reg, inp, index_reg + 1, index_inp + 1)) == bool:
            return False
        return inp[index_inp] + word(reg, inp, index_reg + 1, index_inp + 1)
    if reg[index_reg] == '+':
        if reg[index_reg - 1] == '.' and inp[index_inp] == inp[index_inp - 1]:
            return inp[index_inp] + word(reg, inp, index_reg, index_inp + 1)
        if reg[index_reg - 1] == '.':
            return word(reg, inp, index_reg + 1, index_inp)
        if single_char(reg[index_reg - 1], inp[index_inp]):
            return inp[index_inp] + word(reg, inp, index_reg, index_inp + 1)
        return word(reg, inp, index_reg + 1, index_inp)
    # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
    if single_char(reg[index_reg], inp[index_inp]):
        if type(word(reg, inp, index_reg + 1, index_inp + 1)) == bool:
            return False
        return inp[index_inp] + word(reg, inp, index_reg + 1, index_inp + 1)
    return False


def all_words(reg, inp, index_reg=0, index_inp=0):
    """Returns list of all matches string"""
    if len(reg) == index_reg:
        return [True]
    if len(inp) == index_inp:
        return [False]
    if word(reg, inp, index_inp=index_inp):
        return [word(reg, inp, index_inp=index_inp)] + all_words(reg, inp, index_inp=index_inp + 1)
    if len(inp) == index_inp:
        return [None]
    return all_words(reg, inp, index_inp=index_inp + 1)


def start_end_operators(reg, inp):
    """Realisation of ^ and $ operators"""
    if reg.startswith('^') and reg.endswith('$'):
        if len(all_words(reg[1:-1], inp)) == 2 and all_words(reg[1:-1], inp)[0] == inp:
            return True
        return False
    if reg.startswith('^'):
        return bool(word(reg[1:], inp, index_inp=0))
    if reg.endswith('$') and not reg.endswith('\\$'):
        return inp.endswith(all_words(reg[:-1], inp)[-2])
    return all_words(reg, inp)[0]


def regexp(reg, inp):
    """Wrapper"""
    return bool(start_end_operators(reg, inp))


print(regexp(*input().split('|')))
