"""
LL(1) and CYK parser for formal languages class.

Author: Claire Hardgrove
"""
# TODO: Stop hardcoding the parse table

# access an element of the parse table at M[X, b] using M['X']['b']
# blank entries throw a keyerror
# epsilon is encoded as the empty string

import sys
import re
from collections import defaultdict
import argparse
from os.path import exists

EPSILON = ''
ACCEPTED = 'ACCEPTED'
REJECTED = 'REJECTED'
ERROR_INVALID_SYMBOL = 'ERROR_INVALID_SYMBOL'
START = 'L'
END = '$'
LL1TABLE = {
    'L': {'(': 'ER', 'a': 'ER', 'b': 'ER', 'c': 'ER', 'd': 'ER', '0': 'ER', \
        '1': 'ER', '2': 'ER', '3': 'ER'},
    'R': {'(': 'ER', ')': EPSILON, 'a': 'ER', 'b': 'ER', 'c': 'ER', 'd': 'ER', \
        '0': 'ER', '1': 'ER', '2': 'ER', '3': 'ER', '$': EPSILON},
    'E': {'(': '(M', 'a': 'V', 'b': 'V', 'c': 'V', 'd': 'V', '0': 'T', \
        '1': 'T', '2': 'T', '3': 'T'},
    'M': {'i': 'C)', '+': 'F)', '-': 'F)', '*': 'F)', 'p': 'F)'},
    'C': {'i': 'ifEEN'},
    'N': {'(': 'E', ')': EPSILON, 'a': 'E', 'b': 'E', 'c': 'E', 'd': 'E', \
        '0': 'E', '1': 'E', '2': 'E', '3': 'E'},
    'F': {'+': '+L', '-': '-L', '*': '*L', 'p': 'printL'},
    'V': {'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd'},
    'T': {'0': '0', '1': '1', '2': '2', '3': '3'}
}
CYKTABLE = {}
TERMINALS = set(['(', ')', 'i', 'f', '+', '-', '*', 'p', 'r', 'i', 'n', 't', \
    'a', 'b', 'c', 'd', '0', '1', '2', '3'])

class Stack:
    """
    Stack class based on
    http://interactivepython.org/courselib/static/pythonds/BasicDS/Implementing\
    aStackinPython.html
    """
    def __init__(self):
        self.items = []

    def is_empty(self):
        """Returns True if the stack is empty"""
        return self.items == []

    def push(self, item):
        """Push an item onto the stack"""
        self.items.append(item)

    def pop(self):
        """Pop an item off the top of the stack"""
        return self.items.pop()

    def peek(self):
        """Look at the top item on the stack without removing it"""
        return self.items[len(self.items)-1]

    def size(self):
        """Return the size of the stack"""
        return len(self.items)

    def __repr__(self):
        return ''.join(reversed(self.items))


class LL1Parser:
    """
    An LL(1) parser. The parse method parses an input string an returns
    whether the string is in the language described by the LL1 table,
    terminals and start symbol given when initialising the class. By default
    this class uses the grammar G' from the COMP2022 Assignment 2.
    """

    def __init__(self, table=LL1TABLE, terminals=TERMINALS, start=START,
                 end=END, error_invalid_symbol=ERROR_INVALID_SYMBOL):
        self.table = table
        self.terminals = terminals
        self.start = start
        self.end = end
        self.stack = Stack()
        self.error_invalid_symbol = error_invalid_symbol

    def read_input(self, path):
        """Read and strip all whitespace from input"""
        with open(path) as file:
            string = ''.join([re.sub(r'\s+', '', line) for line in file.readlines()])
        return string

    def is_valid(self, string):
        """
        Returns true if all symbols in the string are in the set of terminals
        """
        return set(string).issubset(self.terminals)

    def is_terminal(self, token):
        """Returns true if a symbol is in the list of terminals"""
        return token in self.terminals

    def tokenize(self, entry):
        """
        Turns an entry from a parse table into a list of symbols that can be
        pushed onto the Stack
        """
        return list(entry)

    def is_variable(self, item):
        """Returns true if a symbol is a variable"""
        return item in self.table.keys()

    def is_entry(self, variable, token):
        """
        Returns True if the parse table has an entry for variable V and
        terminal a at position M[V][a], otherwise a KeyError will be raised and
        this method returns False.
        """
        if variable in self.table and token in self.table[variable]:
            return True
        return False

    def get_entry(self, variable, token):
        """
        Get the entry at position M[V][a] in the parse table for variable V
        and terminal a
        """
        try:
            return self.table[variable][token]
        except KeyError:
            raise IndexError("No entry M[{variable},{token}]".format(
                variable=variable, token=token))

    def parse(self, infile):
        """
        LL(1) Parser reads the input file, stripping whitespace, then checks if
        every symbol in the input file is in the list of terminals for the
        parser's grammar, and finally implements the algorithm described in
        COMP2022 Lectures for parsing an LL(1) grammar (enumerated in comments
        below). The parse method returns True if the string in the input file
        is in the language, otherwise it returns False.
        """

        string = self.read_input(infile)

        # check if input contains only terminals from the grammar
        if not self.is_valid(string):
            print(self.error_invalid_symbol)
            sys.exit(0)

        # 1. append '$' to the input and push '$' to the stack
        string = string + self.end
        self.stack.push(self.end)

        # 2. push the start variable on the stack and scan the first token
        self.stack.push(self.start)
        index = 0 # token will be scanned when loop starts

        # 3. Repeat
        while not self.stack.is_empty():
            token = string[index]
            print(string[index:], self.stack)
            #3.1 If the top of the stack is a variable symbol V , and the current
            #token is a, then pop V and push the string from the table
            #entry (V , a). If the entry was empty, reject the input.
            top_of_stack = self.stack.peek()
            if self.is_variable(top_of_stack):
                if self.is_entry(top_of_stack, token):
                    self.stack.pop()
                    # push on the stack the chars in table[top_of_stack, token] in reverse order
                    entry = self.get_entry(top_of_stack, token)
                    for char in reversed(self.tokenize(entry)):
                        self.stack.push(char)
                else:
                    return False
            #3.2 else if the top of the stack is a terminal symbol t, compare t
            #to a. If they match, pop the stack and scan the next token.
            #Otherwise, reject the input.
            elif self.is_terminal(top_of_stack):
                if top_of_stack == token:
                    self.stack.pop()
                    index += 1
                else:
                    return False
            #3.3 else if the top of the stack and the token are both $, then
            #accept the input (the stack is empty and we have used all the
            #input.)
            elif top_of_stack == self.end and token == self.end:
                break
            #3.4 else reject the input (the stack is empty but there is unread
            #input.)
            else:
                return False
        # return True if the string has not already been rejected
        return True

class CNFError(Exception):
    """An error that is raised if a token is not in the grammar"""
    def __init__(self, rule):
        self.rule = rule

    def __str__(self):
        return "Grammar is not in CNF (Rule {rule})".format(rule=self.rule)


class CYKTable:
    """
    A triangular matrix of the right size to parse `string`
    :param: string A list of tokens representing the string that needs to be
            parsed.
    """

    def __init__(self, string):
        self.table = [[[] for c in range(0, r)] for r in range(len(string), 0, -1)]

    def __repr__(self):
        return '\n'.join(reversed(["{i}: {stringified_row}".format(
            i=i, stringified_row=[str(node) for node in row]) \
            for i, row in enumerate(self.table)]))

    def __getitem__(self, rowcolumn):
        row, column = rowcolumn
        length = len(self.table)
        if row < 0:
            row += length
        if column < 0:
            column += length
        if 0 <= row < length and 0 <= column < length - row:
            return self.table[row][column]
        raise IndexError("Index out of range: [{row}, {column}]".format(
            row=row, column=column))

    def __setitem__(self, rowcolumn, value):
        row, column = rowcolumn
        length = len(self.table)
        if row < 0:
            row += length
        if column < 0:
            column += length
        if 0 <= row < length and 0 <= column < length - row:
            self.table[row][column] = value
            return
        raise IndexError("Index out of range: [{row}, {column}]".format(
            row=row, column=column))

class CYKNode:
    """
    A node of a binary search tree used to store information about the
    production rule used to populate an entry of a CYKTable in order to
    reconstruct a binary search tree from the table.
    For nonterminal rules, the Node contains Ra at the root and the children
    Rb, Rc from the right hand side
    of the rule Ra -> Rb Rc. Rules of the form
    Ra -> b used to construct terminal symbols will only have a left child.
    """

    def __init__(self, symbol, left=None, right=None):
        self.symbol = symbol
        self.left = left
        self.right = right

    def __repr__(self):
        return "{symbol}".format(symbol=self.symbol)

    def get_symbol(self):
        """Get the symbol at the root of this node"""
        return self.symbol

    def get_left(self):
        """Get the left part of the right hand side of the rule"""
        return self.left

    def get_right(self):
        """Get the right part of the right hand side of the rule"""
        return self.right

    def is_unit_rule(self):
        """Return True if the current node represents a unit production rule"""
        return self.left is not None and self.right is None

    def is_terminal(self):
        """Return True if the current node represents a terminal symbol"""
        return self.left is None and self.right is None

class CYKParser:
    """
    The CYKParser expects a grammar file, from which it constructs the lists
    of rules that will be used to parse a string. Each rule in the grammar file
    consist of a token on the left hand side and a list of one terminal
    token or two variable tokens on the right hand side separated by spaces.
    The tokens may be more than one character long, since a grammar might
    include more variables than the number of uppercase letters.

    The method `parse` is used to parse an input string, and prints the tree
    generated by the string for unambiguous grammars. The method `recognise`
    merely recognises the string, and prints the parse table generated while
    recognising the string.

    This parser does not handle ambigous grammars.
    """

    def __init__(self, grammar_file, error_invalid_symbol=ERROR_INVALID_SYMBOL):
        self.rules = None
        self.unit_productions = defaultdict(list)
        self.nonterminal_rules = []
        self.error_invalid_symbol = error_invalid_symbol
        self.start_symbol = None
        # add the rules from the grammar to terminal and variable rules
        self._read_grammar(grammar_file)

    def is_valid(self, string):
        """
        Returns True if all tokens in the string are terminals from the
        grammar
        """
        for token in string:
            if not token in self.unit_productions:
                return False
        return True

    def _read_grammar(self, grammar_file):
        """
        Reads a grammar file and appends the rules to the list of
        terminal and nonterminal rules in the grammar. The start symbol
        must be the LHS of the first rule in the file.
        """
        grammar_rhs = lambda rule: rule.strip().split('->')[1].strip()
        grammar_lhs = lambda rule: rule.strip().split('->')[0].strip()
        with open(grammar_file) as file:
            lines = file.readlines()
        self.start_symbol = grammar_lhs(lines[0])
        for line in lines:
            # Get and check the LHS of the rule
            lhs = grammar_lhs(line)
            if len(grammar_lhs(line).split(' ')) != 1:
                raise CNFError(line)
            # Get the RHSes for this LHS
            multirule_rhs = [rule.strip().split(' ') for rule in grammar_rhs(line).split('|')]
            for rule in multirule_rhs:
                if len(rule) == 1:
                    self.unit_productions[rule[0]].append(lhs)
                elif len(rule) == 2:
                    self.nonterminal_rules.append((lhs, rule))
                else:
                    raise CNFError("{lhs} -> {rule}".format(lhs=lhs, rule=rule))

    def read_input(self, path):
        """Read and strip all whitespace from input"""
        with open(path) as file:
            string = ''.join([re.sub(r'\s+', '', line) for line in file.readlines()])
        return string

    def _generate_tree(self, node):
        """Print the tree with node at the root"""
        if node.is_terminal():
            return node.get_symbol()
        if node.is_unit_rule():
            return [node.get_symbol(),
                    self._generate_tree(node.get_left()),
                    None]
        return [node.get_symbol(),
                self._generate_tree(node.get_left()),
                self._generate_tree(node.get_right())]

    def recognise(self, infile):
        """
        Print the parse table and returns True if a string is in the language,
        otherwise return False
        """
        string = self.read_input(infile)
        table = CYKTable(string)
        # Fill the first row of the matrix with the variables
        # that could have created the terminal at that position
        # in the string. All the terminals are stored in the
        # dictionary `unit_productions` along with the list of
        # terminals that could create them, so just add this
        # list to the table.
        len_string = len(string)
        for start in range(0, len_string):
            try:
                table[0, start] = table[0, start] = self.unit_productions[string[start]]
            # Reject the string if it contains a symbol for which there is no unit production
            except KeyError:
                return False
        # Find the rules that could have generated each substring
        # and add them to the table.
        for length in range(2, len_string+1): # length of span
            for start in range(0, len_string-length+1): # start of span
                for partition in range(1, length-1+1): # partition of span
                    for lhs, rhs in self.nonterminal_rules:
                        if rhs[0] in table[partition-1, start] and \
                            rhs[1] in table[(length-partition)-1,
                                            start+partition]: # don't decrement
                            table[length-1, start].append(lhs)

        # If the start symbol is in the last cell then return True
        # Empty string will cause an index error so check that length of string (n) > 0
        if len_string > 0 and self.start_symbol in table[len_string-1, 0]:
            print(table)
            return True
        return False

    def parse(self, infile):
        """
        Reads and formats the string from the input file, initialises a table
        for parsing the string, and parses the string using the CYK Algorithm:

        Wikipedia:
        for each s = 1 to n
          for each unit production Rv -> as
              set P[1,s,v] = true -> i.e. add Rv to table[1, s]
        for each l = 2 to n -- Length of span
          for each s = 1 to n-l+1 -- Start of span
              for each p = 1 to l-1 -- Partition of span
                  for each production Ra -> Rb Rc
                      if P[p,s,b] and P[l-p,s+p,c] then set P[l,s,a] = true
        if P[n,1,1] is true then
          accept the string
        else reject the string

        Instead of using a three dimensional matrix, the variable Rk is stored
        at position P[i,j] iff P[i,j,k] is true.

        To allow the parse tree to be reconstructed from the table, instead of
        storing variables in the table, we store binary tree nodes of class CYKNode

        This does not handle ambiguous grammars.
        """
        string = self.read_input(infile)
        # check if input contains only terminals from the grammar
        if not self.is_valid(string):
            print(self.error_invalid_symbol)
            sys.exit(0)

        table = CYKTable(string)
        # Fill the first row of the matrix with the variables
        # that could have created the terminal at that position
        # in the string. All the terminals are stored in the
        # dictionary `unit_productions` along with the list of
        # terminals that could create them, so just add this
        # list to the table.
        len_string = len(string)
        for start in range(0, len_string):
            try:
                table[0, start] = [CYKNode(symbol,
                                           left=CYKNode(string[start])) \
                                   for symbol in \
                                   self.unit_productions[string[start]]]
            # Reject the string if it contains a symbol for which there is no unit production
            except KeyError:
                return False
        # Find the rules that could have generated each substring
        # and add them to the table.
        for length in range(2, len_string+1): # length of span
            for start in range(0, len_string-length+1): # start of span
                for partition in range(1, length-1+1): # partition of span
                    for lhs, rhs in self.nonterminal_rules:
                        # The right hand side of the rule will become
                        # left and right children in the parse tree, if they
                        # can be found in the right cells in the table
                        left_child_symbol, right_child_symbol = rhs[0], rhs[1]
                        # We will look in these cells to find the left and right
                        # symbols from the right hand side of the rule
                        search_left = table[partition-1, start]
                        search_right = table[(length-partition)-1, start+partition]
                        # Get the next item in search_left/search_right that
                        # matches left_child_symbol/right_child_symbol (there
                        # should only be one)
                        left_child = next((node for node in search_left if \
                            node.get_symbol() == left_child_symbol), None)
                        right_child = next((node for node in search_right if \
                            node.get_symbol() == right_child_symbol), None)
                        # If we found a left child and right child in the right
                        # places we add them as children of the variable on the
                        # left hand side of the rule and enter the node representing
                        # that rule into the table.
                        if left_child and right_child:
                            table[length-1, start].extend([CYKNode(lhs, left_child, right_child)])


        # If the start symbol is in the last cell then return True
        # Empty string will cause an index error so check that length of string (n) > 0
        if len_string > 0 and self.start_symbol in [node.get_symbol() for node \
            in table[len_string-1, 0]]:
            start_node = next((node for node in table[len_string-1, 0] \
                if node.get_symbol() == self.start_symbol), None)
            print(self._generate_tree(start_node))
            return True
        return False


def main(input_file, cyk=False, grammar=None):
    """
    Select a parser, parse the input given on the command line, and
    print the ACCEPTED or REJECTED message
    """
    parser = LL1Parser() if not cyk else CYKParser(grammar)
    accepted = parser.parse(input_file)
    if accepted:
        print(ACCEPTED)
    else:
        print(REJECTED)


if __name__ == '__main__':
    ARGPARSER = argparse.ArgumentParser(description='Parse a string in an input \
                                     file.')
    ARGPARSER.add_argument('input_file',
                           help='The file containing the string to parse. \
                           Whitespace will be stripped from the file before \
                           parsing')
    ARGPARSER.add_argument('--cyk',
                           help='Add this flag to use the CYK parser. Requires \
                           a grammar file')

    ARGS = ARGPARSER.parse_args()
    INPUT_FILE = ARGS.input_file
    if INPUT_FILE is None:
        ARGPARSER.print_help()
    if not exists(INPUT_FILE):
        raise FileNotFoundError
    CYK = ARGS.cyk if ARGS.cyk else None
    GRAMMAR = CYK if CYK is not None else None
    main(INPUT_FILE, CYK, GRAMMAR)
