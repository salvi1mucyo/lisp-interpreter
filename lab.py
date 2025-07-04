"""
6.101 Lab:
LISP Interpreter Part 2
"""

#!/usr/bin/env python3
import sys

sys.setrecursionlimit(20_000)


#############################
# Scheme-related Exceptions #
#############################


class SchemeError(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class SchemeSyntaxError(SchemeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class SchemeNameError(SchemeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class SchemeEvaluationError(SchemeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """

    pass


############################
# Tokenization and Parsing #
############################


def number_or_symbol(value):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    """
    out = []
    lines = source.split("\n")
    for line in lines:
        comment_ind = line.find(";")
        if comment_ind != -1:
            line = line[:comment_ind]
        new_line = ""
        for char in line:
            if char in "()":
                new_line += " " + char + " "
            else:
                new_line += char
        out.extend([char for char in new_line.split(" ") if char != ""])
    return out


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    count = 0
    finished = False
    if len(tokens) > 1 and tokens[0] != "(":
        raise SchemeSyntaxError
    for token in tokens:
        if finished:
            raise SchemeSyntaxError
        if token == "(":
            count += 1
        if token == ")":
            if count == 0:
                raise SchemeSyntaxError
            count -= 1
            if count == 0:
                finished = True
    if count != 0:
        raise SchemeSyntaxError

    def parse_helper(index):
        token = tokens[index]
        if number_or_symbol(token) != "(":
            return number_or_symbol(token), index + 1
        next_index = index + 1
        out = []
        while tokens[next_index] != ")":
            current_expression, next_index = parse_helper(next_index)
            out.append(current_expression)
        return out, next_index + 1

    parsed_tokens = parse_helper(0)[0]

    return parsed_tokens


######################
# Built-in Functions #
######################


def calc_sub(*args):
    """
    Subtracts arguments
    """
    if len(args) == 1:
        return -args[0]

    first_num, *rest_nums = args
    return first_num - scheme_builtins["+"](*rest_nums)


def calc_mul(*args):
    """
    Multiplies arguments
    """
    product = 1
    for num in args:
        product *= num
    return product


def calc_div(*args):
    """
    Divides arguments
    """
    if len(args) == 0:
        raise SchemeEvaluationError("No arguments were provided when dividing")
    if len(args) == 1:
        return 1 / args[0]
    first, *rest = args
    return first / calc_mul(*rest)


def binary_op(op):
    """
    Returns a binary operator function
    """

    def operation(*args):
        current = args[0]
        for arg in args[1:]:
            if not op(current, arg):
                return False
            current = arg
        return True

    return operation


def evaluate_not(*args):
    """
    Negates the expression
    """
    if len(args) != 1:
        raise SchemeEvaluationError
    return not args[0]


def get_car(*args):
    """
    returns the car attribute of a pair instance
    """
    if len(args) != 1 or not isinstance(args[0], Pair):
        raise SchemeEvaluationError
    return args[0].car


def get_cdr(*args):
    """
    returns the cdr attribute of a pair instance
    """
    if len(args) != 1 or not isinstance(args[0], Pair):
        raise SchemeEvaluationError
    return args[0].cdr


def append(*args):
    """
    Returns a new linked list that returns from appending the given
    linked lists as arguments
    """
    out = LinkedList(None, None)
    for linked_list in args:
        if linked_list is None:
            continue
        if not isinstance(linked_list, LinkedList):
            raise SchemeEvaluationError
        out.append(linked_list.copy())
    return out.cdr


def length(*args):
    """
    Returs the length of a linked list
    """
    if len(args) != 1:
        raise SchemeEvaluationError
    obj = args[0]
    if obj is None:
        return 0
    if isinstance(obj, LinkedList):
        return len(obj)
    else:
        raise SchemeEvaluationError


def list_ref(*args):
    """
    Returns the value at an index in a linked list
    """
    if len(args) != 2:
        raise SchemeEvaluationError
    obj = args[0]
    index = args[1]
    if not isinstance(obj, Pair):
        raise SchemeEvaluationError("Object must be a cons")
    return obj[index]


def is_list(*args):
    """
    Returns whether the given argument is a list
    """
    if len(args) != 1:
        raise SchemeEvaluationError
    obj = args[0]
    return isinstance(obj, LinkedList) or obj is None


def create_list(*args):
    """
    Creates a new list from the provided arguments
    """
    if not args:
        return None
    current_list = LinkedList(args[0], None)
    for element in args[1:]:
        current_list.append(LinkedList(element, None))
    return current_list


def create_cons(*args):
    """
    Creates a cons pair from the provided arguments
    """
    if len(args) != 2:
        raise SchemeEvaluationError("Cons should have 2 attributes")

    if isinstance(args[1], LinkedList) or args[1] is None:
        return LinkedList(args[0], args[1])
    return Pair(args[0], args[1])


def begin(*args):
    """
    Returns the last expression that is evaluated
    """
    return args[-1]


scheme_builtins = {
    "+": lambda *args: sum(args),
    "-": calc_sub,
    "*": calc_mul,
    "/": calc_div,
    "equal?": binary_op(lambda x, y: x == y),
    ">": binary_op(lambda x, y: x > y),
    "<": binary_op(lambda x, y: x < y),
    ">=": binary_op(lambda x, y: x >= y),
    "<=": binary_op(lambda x, y: x <= y),
    "#t": True,
    "#f": False,
    "not": evaluate_not,
    "car": get_car,
    "cdr": get_cdr,
    "append": append,
    "length": length,
    "list-ref": list_ref,
    "list?": is_list,
    "list": create_list,
    "cons": create_cons,
    "begin": begin,
}

#################
# special forms #
#################


def special_lambda(tree, frame):
    """
    Creates a new function object
    """
    parameters = tree[1]
    code = tree[2]
    return UserFunction(frame, parameters, code)


def special_define(tree, frame):
    """
    Defines a variable or a function
    """
    name = tree[1]
    # if you are defining a function, return a function object
    if isinstance(name, list):
        parameters = name[1:]
        code = tree[2]
        name = name[0]
        value = UserFunction(frame, parameters, code)
        frame[name] = value
        return value
    # assign variable to evaluated object
    value = evaluate(tree[2], frame)
    frame[name] = value
    return value


def special_if(tree, frame):
    """
    if conditional
    """
    pred = evaluate(tree[1], frame)
    if pred:
        return evaluate(tree[2], frame)
    else:
        return evaluate(tree[3], frame)


def special_and(tree, frame):
    """
    and combinator
    """
    for arg in tree[1:]:
        if not evaluate(arg, frame):
            return False
    return True


def special_or(tree, frame):
    """
    or combinator
    """
    for arg in tree[1:]:
        if evaluate(arg, frame):
            return True
    return False


def special_del(tree, frame):
    """
    deletes the given variable in the current frame
    """
    name = tree[1]
    if name in frame:
        obj = frame[name]
        del frame[name]
        return obj
    else:
        raise SchemeNameError


def special_let(tree, frame):
    """
    Creates a new function object and evaluates it
    """
    new_expression = []
    function_obj = ["lambda"]
    parameters = []
    mappings = tree[1]
    body = tree[2]
    arguments = []
    for param, arg in mappings:
        parameters.append(param)
        arguments.append(arg)
    function_obj.append(parameters)
    function_obj.append(body)
    new_expression = [function_obj] + arguments
    return evaluate(new_expression, frame)


def special_setbang(tree, frame):
    """
    Assigns the value to the variable in the closest frame
    """
    variable, value = tree[1], evaluate(tree[2], frame)
    frame_with_var = frame.getframe(variable)
    frame_with_var[variable] = value
    return value


special_forms = {
    "lambda": special_lambda,
    "define": special_define,
    "if": special_if,
    "and": special_and,
    "or": special_or,
    "del": special_del,
    "let": special_let,
    "set!": special_setbang,
}


########################
# Frames and Functions #
########################


class Frame:
    """
    This class represents a frame in the stack.
    It contains a pointer to the parent frame and a mapping of the variables
    to their objects
    """

    def __init__(self, parent=None):
        self.parent = parent
        self.variables = {}

    def __contains__(self, variable):
        return variable in self.variables

    def __getitem__(self, variable):
        if variable in self:
            return self.variables[variable]

        # if you have reached the builtin frame and haven't found the variable,
        # raise an error
        if self.parent is None:
            raise SchemeNameError(f"name '{variable}' is not defined")

        # lookup in parent frame
        return self.parent[variable]

    def __setitem__(self, variable, value):
        self.variables[variable] = value

    def __delitem__(self, variable):
        del self.variables[variable]

    def getframe(self, variable):
        """
        Returns the closest frame with the given varible
        """
        if variable in self:
            return self

        # if you have reached the builtin frame and haven't found the variable,
        # raise an error
        if self.parent is None:
            raise SchemeNameError(f"name '{variable}' is not defined")

        # lookup in parent frame
        return self.parent.getframe(variable)


class UserFunction:
    """
    This class represents a function object created by the user.
    It contains a pointer to the enclosing frame in which it was created,
    parameters, and the body code of the the function
    """

    def __init__(self, enclosing_frame, parameters, code):
        self.enclosing_frame = enclosing_frame
        self.parameters = parameters
        self.code = code

    def __call__(self, *args, **kwds):
        if len(args) != len(self.parameters):
            raise SchemeEvaluationError(
                f"Expected {len(self.parameters)} arguments, got {len(args)}"
            )
        frame = Frame(self.enclosing_frame)
        for par, arg in zip(self.parameters, args):
            frame[par] = arg
        return evaluate(self.code, frame)


class Pair:
    """
    This class represents a cons pair
    """

    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

    def __getitem__(self, index):
        if index == 0:
            return self.car
        if not isinstance(self.cdr, Pair):
            raise SchemeEvaluationError
        return self.cdr[index - 1]


class LinkedList(Pair):
    """
    This class represents a linked list
    """

    def __len__(self):
        counter = 0
        current = self
        while current is not None:
            counter += 1
            current = get_cdr(current)
        return counter

    def copy(self):
        if self.cdr is None:
            return LinkedList(self.car, None)
        return LinkedList(self.car, self.cdr.copy())

    def append(self, input_list):
        current = self
        while current.cdr is not None:
            current = current.cdr
        current.cdr = input_list

    def __str__(self):
        if self.cdr is None:
            return f"(list {self.car})"
        return f"(list {self.car}" + str(self.cdr)[5:]


##############
# Evaluation #
##############


def evaluate(tree, frame=None):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
    if frame is None:
        frame = make_initial_frame()
    if isinstance(tree, (int, float)):
        return tree
    if isinstance(tree, str):
        try:
            return frame[tree]
        except KeyError:
            raise SchemeNameError(f"name '{tree}' is not defined")
    if len(tree) == 0:
        return None
    first = tree[0]
    if isinstance(first, str) and first in special_forms:
        return special_forms[first](tree, frame)

    # functions
    operation = evaluate(first, frame)

    # if the first element does evaluate to a function, raise an error
    try:
        return operation(*[evaluate(exp, frame) for exp in tree[1:]])
    except TypeError:
        raise SchemeEvaluationError(f"{type(operation)} is not a callable function")


def evaluate_file(filename, frame=None):
    if frame is None:
        frame = make_initial_frame()
    with open(filename, "r", encoding="utf-8") as f:
        source = f.read()
        return evaluate(parse(tokenize(source)), frame)


def make_initial_frame():
    builtin_frame = Frame()
    for op, func in scheme_builtins.items():
        builtin_frame[op] = func
    return Frame(builtin_frame)


if __name__ == "__main__":
    import os

    sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))
    import schemerepl

    initial_frame = make_initial_frame()
    if len(sys.argv) != 1:
        files = sys.argv[1:]
        for file in files:
            evaluate_file(file, initial_frame)
    schemerepl.SchemeREPL(
        sys.modules[__name__], use_frames=True, verbose=False, repl_frame=initial_frame
    ).cmdloop()
