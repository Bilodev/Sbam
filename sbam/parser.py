from utils.tkn import Token
from utils.variable import Variable


libs: dict[str, set] = {
    'sbam!': {'println!', 'print!', 'scan!'}
}


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


class Parser:

    keywords = {
        'if',
        'elif',
        'while',
        'else',
        'for',
        'import',
        'let',
        'true',
        'false', 'break', 'continue', 'in'}

    operators = {
        '+',
        '-',
        '*',
        '%',
        '/',
        '!=',
        '<',
        '<=',
        '>',
        '>=',
        '=',
        '==',
        'not',
        'and',
        'or'}

    symbols = {'.', '..', ':', '(', ')', '{', '}'}

    types = {'integer', 'float', 'string', 'boolean'}

    valid_tokens = keywords.union(operators).union(types).union(symbols)

    def analyze_declarations(self):

        for n_line, l in enumerate(self.splitted_lines):

            if 'let' not in l:
                continue

            # controllo operazioni let a : integer = 4+43

            if len(l) > 5:
                to_sum = l[5:]
                for i, e in enumerate(to_sum):

                    if e == 'false':
                        to_sum[i] = '0'
                    elif e == 'true':
                        to_sum[i] = '1'

                    for v in self.vars:
                        if e == v.name:
                            to_sum[i] = v.value

                to_sum = "".join(to_sum)

                if 'boolean' in l:
                    l[5] = l[5].replace('0', 'false').replace('1', 'true')

                elif 'string' not in l:
                    l[5] = str(eval(to_sum))
                elif 'string' in l:
                    l[5] = "'" + (str(eval(to_sum))) + "'"

            # controllo dichiarazioni : let a : integer

            if len(l) == 4:
                let, name, d_p, type_ = l
                l.append('=')
                if type_ == 'integer':
                    l.append('0')
                elif type_ == 'boolean':
                    l.append('false')
                elif type_ == 'float':
                    l.append('.0')
                elif type_ == 'string':
                    l.append("''")

            else:
                let, name, d_p, type_, equals = l[:5]

            if '!' in name or '.' in name or name in self.valid_tokens:
                print(
                    f"Naming Error: {name!r} cannot contain chars like '!' or '.', cant be a keyword ,Line: {n_line+1}")
                exit(-1)

            if not (
                    let == 'let',
                    d_p == ':',
                    type_ in self.types,
                    equals == '='):
                continue

            valid = False

            for v in self.vars:
                if l[5] == v.name:
                    l[5] = v.value

            if type_ == 'string' and l[5].startswith(
                    "'") and l[5].endswith("'"):
                valid = True

            elif type_ == 'boolean' and l[5] in ('true', 'false'):
                valid = True

            elif (type_ == 'integer') and ('"' not in l[5]) and ("'" not in l[5]) and (float(l[5]) == 0 or float(l[5])):
                valid = True

            elif (type_ == 'float') and ('"' not in l[5]) and ("'" not in l[5]) and (float(l[5]) == 0 or float(l[5])):
                valid = True

            if valid:
                if name not in [v.name for v in self.vars]:
                    self.vars.append(Variable(type_, l[5], name))
                else:
                    print(
                        f'Variable {name!r} already existing, cannot re-declare it on line {n_line+1}')
                    exit(-1)

    def analyze_apices(self):
        apices_counter = 0
        last_line = 0
        for t in self.tokens:
            for c in t.token:
                if c == "'":
                    last_line = t.line
                    apices_counter += 1

        if apices_counter % 2 != 0:
            print(f'Apices Error, apices not closed on line {last_line+1}')
            exit(-1)

    def analyze_parenthesis(self):

        open_p = 0

        open_g = 0

        for t in self.tokens:
            if t.token == '(':
                open_p += 1

            elif t.token == '{':
                open_g += 1

            elif t.token == ')':
                open_p -= 1

            elif t.token == '}':
                open_g -= 1

        if not (open_p == open_g == 0):
            print(f'Syntax Error: Parenthesis on line {0}')
            exit(-1)

    def analyze_operators(self):
        ope_lines = []
        for l in self.splitted_lines:
            for ope in self.operators:
                if ope in l and '=' not in l and 'let' not in l:
                    ope_lines.append(l)

        for l in ope_lines:
            for i, element in enumerate(l):
                for v in self.vars:
                    if v.name == element:
                        if v.value == 'false':
                            l[i] = '0'
                        elif v.value == 'true':
                            l[i] = '1'
                        else:
                            l[i] = v.value

        # separare le operazioni dal resto

        separated_ops = []
        for i, l in enumerate(ope_lines):
            separated_ops.append([])
            for token in l:

                if is_number(token) or (
                        token[0] == token[-1] == "'") or token in self.operators or token in ('false', 'true'):
                    if token == 'false':
                        separated_ops[i].append('0')
                    elif token == 'true':
                        separated_ops[i].append('1')
                    elif token.isalpha():
                        separated_ops[i].append(' ' + token + ' ')
                    else:
                        separated_ops[i].append(token)

        for op in separated_ops:
            try:
                eval(''.join(op))
            except BaseException:
                print(
                    f'Operation Error, {"".join(op)!r} is not an operation')
                exit(-1)

    def analyze_assignments(self):

        for i, line in enumerate(self.splitted_lines):
            for v in self.vars:

                if not (
                        v.name in line and 'let' not in line and '=' in line):
                    continue

                # +=, -=, /=, *=

                if (line[1] in ('+', '-', '*', '/') and line[2] == '='):
                    line[1], line[2] = line[2], line[1]
                    line.insert(2, v.name)

                # replace delle var nell'assegnazione

                if line[0] == v.name and line[1] == '=':
                    new_value = line[2:]
                    for i, e in enumerate(new_value):
                        for v1 in self.vars:
                            if e == v1.name and (e[0] != "'" != e[-1]):
                                new_value[i] = v1.value

                    new_value = "".join(new_value)

                    if v.type_ == 'string':
                        v.value = "'" + str(eval(new_value)) + "'"

                    elif v.type_ == 'integer':
                        v.value = str(int(eval(new_value)))

                    elif v.type_ == 'float':
                        v.value = str(float(eval(new_value)))

                    elif v.type_ == 'boolean':
                        new_value = new_value.replace(
                            'false', 'False').replace(
                            'true', 'True')
                        v.value = str(bool(eval(new_value)))
                    continue

                # valore singolo

                if len(line) != 3:
                    continue

                name, equals, value = line

                if not (name == v.name and equals == '='):
                    continue

                valid = False

                if v.type_ == 'string' and value.startswith(
                        "'") and value.endswith("'"):
                    valid = True

                elif v.type_ == 'boolean' and value in ('true', 'false'):
                    valid = True

                elif v.type_ == 'integer' and '"' not in line and "'" not in line and int(value):
                    valid = True

                elif v.type_ == 'float' and '"' not in line and "'" not in line and float(value):
                    valid = True

                if valid:
                    v.value = value
                else:
                    print(f'Re-Assigning Error {i+1}')
                    exit(-1)

    def analyze_imports(self):

        importing = True
        line_of_importing = 0

        for t in self.tokens:
            if t.token == 'import':
                importing = True
                line_of_importing = t.line

            if importing and t.token in libs.keys() and t.line == line_of_importing:

                line_of_importing = 0
                importing = False

                lib = libs.get(t.token)
                if lib:
                    self.valid_tokens = self.valid_tokens.union(lib)

    def analyze_constructs(self):

        conditions = []
        flag = False

        # if, while, elif

        for i, l in enumerate(self.splitted_lines):
            if ('if' in l) or ('while' in l) or ('elif' in l) or ('for' in l):

                # check della parentesi graffa aperta

                if '{' not in l:

                    for other_line in range(i + 1, len(self.splitted_lines)):
                        if self.splitted_lines[other_line] != []:
                            if '{' not in self.splitted_lines[other_line]:
                                print('Errore nel costrutto parentesi non chiusa')
                            else:
                                break

                if 'for' in l:

                    if (l[1].isalnum() and not l[1]
                            [0].isdigit()) and l[2] == 'in':
                        if l[1] not in [v.name for v in self.vars]:

                            range_ = ("".join(l[3:]).replace('{', ''))
                            if '..' in range_:
                                dot_dot_index = range_.index('..')
                                n1 = range_[0: dot_dot_index]
                                n2 = range_[dot_dot_index + 2:]

                                for v in self.vars:
                                    if n1 == v.name and v.type_ in (
                                            'integer'):
                                        n1 = v.value

                                    if n2 == v.name and v.type_ in (
                                            'integer'):
                                        n2 = v.value

                                print(n1, n2)
                                if is_number(n1) and is_number(n2):
                                    # aggiunta variabile del for
                                    self.vars.append(
                                        Variable('integer', f'{n1}', l[1]))
                                    continue

                                else:
                                    print('For Error')
                                    exit(-1)

                conditions.append([])
                flag = True

                for token in l:

                    # sostituzione variabili

                    for v in self.vars:
                        if token == v.name:
                            token = v.value

                    # check condizione

                    if is_number(token) or (
                            token[0] == "'" == token[-1]) or token in self.operators or token in ('false', 'true'):

                        if token == 'false':
                            conditions[-1].append('0')
                        elif token == 'true':
                            conditions[-1].append('1')
                        elif token.isalnum():
                            conditions[-1].append(' ' + token + ' ')
                        else:
                            conditions[-1].append(token)

        if flag and [] in conditions:
            print('Cannot use empty conditions')
            exit(-1)

        for c in conditions:
            try:
                bool(eval("".join(c)))
            except BaseException:
                print('Condition is not boolean')

                exit(-1)

    def analyze_functions(self):
        ...

    def analyze_fn_calls(self):
        ...

    def __init__(self, file, tokens: list[Token], splitted_lines) -> None:

        self.file = file

        self.splitted_lines: list[list[str]] = splitted_lines

        self.tokens: list[Token] = tokens

        self.not_verified: list[Token] = []

        self.vars: list[Variable] = []

        self.analyze_imports()

        self.analyze_declarations()

        self.analyze_assignments()

        self.analyze_operators()

        self.analyze_apices()

        self.analyze_parenthesis()

        self.analyze_constructs()

        self.analyze_functions()

        self.analyze_fn_calls()

        for t in tokens:

            if t.token not in self.valid_tokens:

                # skippa stringhe e numeri

                if t.token[0] == "'" and t.token[-1] == "'":
                    continue

                elif is_number(t.token):
                    continue

                # skippa le variabili

                cont = 0
                for v in self.vars:
                    if v.name == t.token:
                        cont = 1
                if cont:
                    continue

                elif t.token in libs.keys():
                    continue

                elif '-' in t.token:
                    continue

                elif '..' in t.token:
                    continue

                # se il token non viene trovato fra i token validi, non rappresenta una stringa
                # o numero, non e una variabile, non viene verificato

                self.not_verified.append(t)

        print(self.vars)

        # token non verificati

        for i in self.not_verified:
            print(f'Token not recognized: {i.token}, Line: {i.line+1}')

        if self.not_verified != []:
            exit(-1)
