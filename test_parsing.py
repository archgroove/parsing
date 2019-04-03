import unittest
# When testing this I called my main file parsing.py, not parser.py
# because there is already a parser module in the Python 3 standard library
import parsing as parsing
import io
import sys

class TestParser(unittest.TestCase):

    # Test LL1 Parser can accept, reject and print invalid
    def test_LL1Parser_accepts_test1(self):
        # input: (if(-1a)(print1))
        input = 'test/test1_accepted'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_LL1Parser_rejects_test3(self):
        # input ()if+-*printabcd0123
        input = 'test/test3_rejected'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_LL1Parser_prints_invalid_test4(self):
        # input: if(9)(print(1+2))
        input = 'test/test4_invalid'
        parser = parsing.LL1Parser()
        # redirect io
        out = io.StringIO()
        sys.stdout = out
        last_output = None
        try:
            accepted = parser.parse(input)
        except SystemExit:
            last_output = [line for line in out.getvalue().strip().split('\n')][-1]
        # get the last line of the output to check string was accepted
        self.assertEqual(last_output, parsing.ERROR_INVALID_SYMBOL)

    def test_LL1Parser_tokenize_epsilon_returns_empty_list(self):
        # Check that when epsilon is encountered in the parse table, the
        # tokenizer turns it into an empty list so that no items from the list
        # are pushed onto the stack.
        entry = ''
        parser = parsing.LL1Parser()
        self.assertEqual(parser.tokenize(entry), [])

    # Test main can print accepted, stack, rejected and invalid text
    def test_LL1Parser_main_prints_accepted_test1(self):
        # input: (if(-1a)(print1))
        input = 'test/test1_accepted'
        out = io.StringIO()
        sys.stdout = out
        result = parsing.main(input)
        # get the last line of the output to check string was accepted
        last_output = [line for line in out.getvalue().strip().split('\n')][-1]
        self.assertEqual(last_output, parsing.ACCEPTED)

    def test_LL1Parser_main_prints_rejected_test3(self):
        # input: ()if+-*printabcd0123
        input = 'test/test3_rejected'
        out = io.StringIO()
        sys.stdout = out
        result = parsing.main(input)
        # get the last line of the output to check string was accepted
        last_output = [line for line in out.getvalue().strip().split('\n')][-1]
        self.assertEqual(last_output, parsing.REJECTED)

    def test_LL1Parser_main_prints_tokens_and_stack_trace_test1(self):
        """
        input: (if(-1a)(print1))
        expected:
        (if(-1a)(print1))$ L$
        (if(-1a)(print1))$ ER$
        (if(-1a)(print1))$ (MR$
        if(-1a)(print1))$ MR$
        if(-1a)(print1))$ C)R$
        if(-1a)(print1))$ ifEEN)R$
        f(-1a)(print1))$ fEEN)R$
        (-1a)(print1))$ EEN)R$
        (-1a)(print1))$ (MEN)R$
        -1a)(print1))$ MEN)R$
        -1a)(print1))$ F)EN)R$
        -1a)(print1))$ -L)EN)R$
        1a)(print1))$ L)EN)R$
        1a)(print1))$ ER)EN)R$
        1a)(print1))$ TR)EN)R$
        1a)(print1))$ 1R)EN)R$
        a)(print1))$ R)EN)R$
        a)(print1))$ ER)EN)R$
        a)(print1))$ VR)EN)R$
        a)(print1))$ aR)EN)R$
        )(print1))$ R)EN)R$
        )(print1))$ )EN)R$
        (print1))$ EN)R$
        (print1))$ (MN)R$
        print1))$ MN)R$
        print1))$ F)N)R$
        print1))$ printL)N)R$
        rint1))$ rintL)N)R$
        int1))$ intL)N)R$
        nt1))$ ntL)N)R$
        t1))$ tL)N)R$
        1))$ L)N)R$
        1))$ ER)N)R$
        1))$ TR)N)R$
        1))$ 1R)N)R$
        ))$ R)N)R$
        ))$ )N)R$
        )$ N)R$
        )$ )R$
        $ R$
        $ $
        ACCEPTED
        """
        input = 'test/test1_accepted'
        expected = 'test/test1_accepted_expected_output'
        with open(expected) as file:
            expected_output = ''.join([line for line in file.readlines()])
        out = io.StringIO()
        sys.stdout = out
        result = parsing.main(input)
        # get the last line of the output to check string was accepted
        output = out.getvalue()
        self.assertEqual(output, expected_output)

    def test_LL1Parser_main_prints_invalid_test4(self):
        # input: if(9)(print(1+2))
        input = 'test/test4_invalid'
        out = io.StringIO()
        sys.stdout = out
        last_output = None
        try:
            result = parsing.main(input)
        except SystemExit:
            last_output = [line for line in out.getvalue().strip().split('\n')][-1]
        # get the last line of the output to check string was accepted
        self.assertEqual(last_output, parsing.ERROR_INVALID_SYMBOL)

    # Test various rejecting strings
    def test_LL1Parser_reject_empty_string(self):
        # input: <no input>
        input = 'test/reject_empty_string'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_LL1Parser_reject_spaces(self):
        # input: <a combination of spaces, tabs and newlines>
        input = 'test/reject_spaces'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_LL1Parser_reject_if_no_parentheses(self):
        # input: if(a1)
        input = 'test/reject_if_no_parentheses'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_LL1Parser_reject_print_no_parentheses(self):
        # input: print1
        input = 'test/reject_print_no_parentheses'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_LL1Parser_reject_minus_plus(self):
        # input: (-+a)
        input = 'test/reject_minus_plus'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_LL1Parser_reject_missing_left_parentheses(self):
        # input: print1)
        input = 'test/reject_missing_left_parentheses'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_LL1Parser_reject_extra_left_parentheses(self):
        # input: ((print1)
        input = 'test/reject_extra_left_parentheses'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_LL1Parser_reject_too_many_parentheses(self):
        # input: ((print1))
        input = 'test/reject_too_many_parentheses'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_LL1Parser_reject_if_missing_expression(self):
        # input: (if(-1))
        input = 'test/reject_if_missing_expression'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    # Test various accepting strings
    def test_LL1Parser_accept_integer_in_range(self):
        # input: 1
        input = 'test/accept_integer_in_range'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_LL1Parser_accept_whitespace_test1(self):
        """
        input:
         (  i   f (   -1 a
             )
            (
        pr    int   1)  )
        """
        input = 'test/accept_whitespace_test1'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_LL1Parser_accept_add_two_expressions(self):
        # input: (+(+a)(-0))
        input = 'test/accept_add_two_expressions'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_LL1Parser_accept_if_statement(self):
        # input: (ifaa)
        input = 'test/accept_if_statement'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_LL1Parser_accept_ifelse_statement(self):
        # input: (ifaaa)
        input = 'test/accept_ifelse_statement'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_LL1Parser_accept_times_expression(self):
        # input: (*a)
        input = 'test/accept_times_expression'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_LL1Parser_accept_times_multiple_expressions(self):
        # input: (*abcd0123)
        input = 'test/accept_times_multiple_expressions'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_LL1Parser_accept_negate_positive(self):
        # input: (-(+a))
        input = 'test/accept_negate_positive'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_LL1Parser_accept_expression(self):
        # input: a
        input = 'test/accept_expression'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_LL1Parser_accept_nested_condition(self):
        # input: (if(ifa0)b)
        input = 'test/accept_nested_condition'
        parser = parsing.LL1Parser()
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    # Test CYKParser
    def test_CYKParser_accepts_test1(self):
        input = 'test/test1_accepted'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_CYKParser_rejects_test3(self):
        input = 'test/test3_rejected'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_CYKParser_prints_invalid_test4(self):
        # Input is same as test1_accepted
        input = 'test/test4_invalid'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        # redirect io
        out = io.StringIO()
        sys.stdout = out
        last_output = None
        try:
            accepted = parser.parse(input)
        except SystemExit:
            last_output = [line for line in out.getvalue().strip().split('\n')][-1]
        # get the last line of the output to check string was accepted
        self.assertEqual(last_output, parsing.ERROR_INVALID_SYMBOL)

    def test_CYKParser_main_prints_accepted(self):
        input = 'test/test6_cyk_unambiguous_accepted'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        #redirect io
        out = io.StringIO()
        sys.stdout = out
        result = parsing.main(input, cyk=True, grammar=grammar)
        output = [line for line in out.getvalue().strip().split('\n')][-1]
        # get the last line of the output to check string was accepted
        self.assertEqual(output, parsing.ACCEPTED)

    # Test various rejecting strings (CYK)
    def test_CYKParser_reject_empty_string(self):
        # input: <no input>
        input = 'test/reject_empty_string'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_CYKParser_reject_spaces(self):
        # input: <a combination of spaces, tabs and newlines>
        input = 'test/reject_spaces'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_CYKParser_reject_if_no_parentheses(self):
        # input: if(a1)
        input = 'test/reject_if_no_parentheses'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_CYKParser_reject_print_no_parentheses(self):
        # input: print1
        input = 'test/reject_print_no_parentheses'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_CYKParser_reject_minus_plus(self):
        # input: (-+a)
        input = 'test/reject_minus_plus'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_CYKParser_reject_missing_left_parentheses(self):
        # input: print1)
        input = 'test/reject_missing_left_parentheses'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_CYKParser_reject_extra_left_parentheses(self):
        # input: ((print1)
        input = 'test/reject_extra_left_parentheses'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_CYKParser_reject_too_many_parentheses(self):
        # input: ((print1))
        input = 'test/reject_too_many_parentheses'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    def test_CYKParser_reject_if_missing_expression(self):
        # input: (if(-1))
        input = 'test/reject_if_missing_expression'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, False)

    # Test various accepting strings (CYK)
    def test_CYKParser_accept_integer_in_range(self):
        # input: 1
        input = 'test/accept_integer_in_range'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_CYKParser_accept_whitespace_test1(self):
        """
        input:
         (  i   f (   -1 a
             )
            (
        pr    int   1)  )
        """
        input = 'test/accept_whitespace_test1'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_CYKParser_accept_add_two_expressions(self):
        # input: (+(+a)(-0))
        input = 'test/accept_add_two_expressions'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_CYKParser_accept_if_statement(self):
        # input: (ifaa)
        input = 'test/accept_if_statement'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_CYKParser_accept_ifelse_statement(self):
        # input: (ifaaa)
        input = 'test/accept_ifelse_statement'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_CYKParser_accept_times_expression(self):
        # input: (*a)
        input = 'test/accept_times_expression'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_CYKParser_accept_times_multiple_expressions(self):
        # input: (*abcd0123)
        input = 'test/accept_times_multiple_expressions'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_CYKParser_accept_negate_positive(self):
        # input: (-(+a))
        input = 'test/accept_negate_positive'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_CYKParser_accept_expression(self):
        # input: a
        input = 'test/accept_expression'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)

    def test_CYKParser_accept_nested_condition(self):
        # input: (if(ifa0)b)
        input = 'test/accept_nested_condition'
        grammar = 'test/test6_cyk_unambiguous_grammar'
        parser = parsing.CYKParser(grammar)
        accepted = parser.parse(input)
        self.assertEqual(accepted, True)
