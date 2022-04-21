#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
    Unit test for taxes

"""

from taxes import tax_bracket, tax_brackets, taxes

import unittest
import mock
from unittest.mock import patch, mock_open, call

class TestTaxBracket(unittest.TestCase):

    def setUp(self):
        pass

    def test_constants(self):
        pass

    def test_init(self):
        brack = tax_bracket(1000, 0.1)
        self.assertEqual(brack.income, 1000)
        self.assertEqual(brack.bracket_size, 1000)
        self.assertEqual(brack.tax_rate, 0.1)

        brack2 = tax_bracket(2000, 0.2, lower_bracket=brack.income)
        self.assertEqual(brack2.income, 2000)
        self.assertEqual(brack2.bracket_size, 1000)
        self.assertEqual(brack2.tax_rate, 0.2)

class TestTaxBrackets(unittest.TestCase):
    def setUp(self):
        pass

    def test_constants(self):
        brack = tax_brackets(0.1)
        pass

    def test_init(self):
        bracks = tax_brackets(0.1)
        self.assertEqual(bracks.top_bracket_tax_rate, 0.1)
        self.assertEqual(bracks.brackets, [])

    def test_init_success(self):
        bracks = tax_brackets(0.3)
        bracks.add_bracket(1000, 0.1)
        self.assertEqual(bracks.brackets[0].income, 1000)
        self.assertEqual(bracks.brackets[0].bracket_size, 1000)
        self.assertEqual(bracks.brackets[0].tax_rate, 0.1)

    def test_add_bracket_easy(self):
        bracks = tax_brackets(0.3)
        bracks.add_bracket(1000, 0.1)
        self.assertEqual(bracks.brackets[0].income, 1000)
        self.assertEqual(bracks.brackets[0].bracket_size, 1000)
        self.assertEqual(bracks.brackets[0].tax_rate, 0.1)
        self.assertEqual(bracks.top_bracket_tax_rate, 0.3)

        bracks.add_bracket(2000, 0.2)
        self.assertEqual(bracks.brackets[0].income, 1000)
        self.assertEqual(bracks.brackets[0].bracket_size, 1000)
        self.assertEqual(bracks.brackets[0].tax_rate, 0.1)
        self.assertEqual(bracks.brackets[1].income, 2000)
        self.assertEqual(bracks.brackets[1].bracket_size, 1000)
        self.assertEqual(bracks.brackets[1].tax_rate, 0.2)
        self.assertEqual(bracks.top_bracket_tax_rate, 0.3)

        bracks.add_bracket(3000, 0.25)
        self.assertEqual(bracks.brackets[0].income, 1000)
        self.assertEqual(bracks.brackets[0].bracket_size, 1000)
        self.assertEqual(bracks.brackets[0].tax_rate, 0.1)
        self.assertEqual(bracks.brackets[1].income, 2000)
        self.assertEqual(bracks.brackets[1].bracket_size, 1000)
        self.assertEqual(bracks.brackets[1].tax_rate, 0.2)
        self.assertEqual(bracks.brackets[2].income, 3000)
        self.assertEqual(bracks.brackets[2].bracket_size, 1000)
        self.assertEqual(bracks.brackets[2].tax_rate, 0.25)
        self.assertEqual(bracks.top_bracket_tax_rate, 0.3)

    def test_add_bracket_reverse(self):
        bracks = tax_brackets(0.3)
        bracks.add_bracket(3000, 0.25)
        self.assertEqual(bracks.brackets[0].income, 3000)
        self.assertEqual(bracks.brackets[0].bracket_size, 3000)
        self.assertEqual(bracks.brackets[0].tax_rate, 0.25)
        self.assertEqual(bracks.top_bracket_tax_rate, 0.3)

        bracks.add_bracket(2000, 0.2)
        self.assertEqual(bracks.brackets[0].income, 2000)
        self.assertEqual(bracks.brackets[0].bracket_size, 2000)
        self.assertEqual(bracks.brackets[0].tax_rate, 0.2)
        self.assertEqual(bracks.brackets[1].income, 3000)
        self.assertEqual(bracks.brackets[1].bracket_size, 1000)
        self.assertEqual(bracks.brackets[1].tax_rate, 0.25)
        self.assertEqual(bracks.top_bracket_tax_rate, 0.3)

        bracks.add_bracket(1000, 0.1)
        self.assertEqual(bracks.brackets[0].income, 1000)
        self.assertEqual(bracks.brackets[0].bracket_size, 1000)
        self.assertEqual(bracks.brackets[0].tax_rate, 0.1)
        self.assertEqual(bracks.brackets[1].income, 2000)
        self.assertEqual(bracks.brackets[1].bracket_size, 1000)
        self.assertEqual(bracks.brackets[1].tax_rate, 0.2)
        self.assertEqual(bracks.brackets[2].income, 3000)
        self.assertEqual(bracks.brackets[2].bracket_size, 1000)
        self.assertEqual(bracks.brackets[2].tax_rate, 0.25)
        self.assertEqual(bracks.top_bracket_tax_rate, 0.3)

    def test_add_bracket_middle(self):
        bracks = tax_brackets(0.3)
        bracks.add_bracket(3000, 0.25)
        self.assertEqual(bracks.brackets[0].income, 3000)
        self.assertEqual(bracks.brackets[0].bracket_size, 3000)
        self.assertEqual(bracks.brackets[0].tax_rate, 0.25)
        self.assertEqual(bracks.top_bracket_tax_rate, 0.3)

        bracks.add_bracket(1000, 0.1)
        self.assertEqual(bracks.brackets[0].income, 1000)
        self.assertEqual(bracks.brackets[0].bracket_size, 1000)
        self.assertEqual(bracks.brackets[0].tax_rate, 0.1)
        self.assertEqual(bracks.brackets[1].income, 3000)
        self.assertEqual(bracks.brackets[1].bracket_size, 2000)
        self.assertEqual(bracks.brackets[1].tax_rate, 0.25)
        self.assertEqual(bracks.top_bracket_tax_rate, 0.3)

        bracks.add_bracket(2000, 0.2)
        self.assertEqual(bracks.brackets[0].income, 1000)
        self.assertEqual(bracks.brackets[0].bracket_size, 1000)
        self.assertEqual(bracks.brackets[0].tax_rate, 0.1)
        self.assertEqual(bracks.brackets[1].income, 2000)
        self.assertEqual(bracks.brackets[1].bracket_size, 1000)
        self.assertEqual(bracks.brackets[1].tax_rate, 0.2)
        self.assertEqual(bracks.brackets[2].income, 3000)
        self.assertEqual(bracks.brackets[2].bracket_size, 1000)
        self.assertEqual(bracks.brackets[2].tax_rate, 0.25)
        self.assertEqual(bracks.top_bracket_tax_rate, 0.3)

    def test_compute_tax(self):
        bracks = tax_brackets(0.3)
        bracks.add_bracket(1000, 0.1)
        bracks.add_bracket(2000, 0.2)
        bracks.add_bracket(3000, 0.25)

        self.assertEqual(100, bracks.compute_tax(1000))
        self.assertEqual(300, bracks.compute_tax(2000))
        self.assertEqual(550, bracks.compute_tax(3000))
        self.assertEqual(850, bracks.compute_tax(4000))

class TestTaxes(unittest.TestCase):
    def setUp(self):
        pass

    def test_constants(self):
        tax = taxes()
        self.assertEqual(tax.provinces[0], "BC")
        self.assertEqual(tax.provinces[1], "AB")
        self.assertEqual(tax.provinces[2], "SK")
        self.assertEqual(tax.provinces[3], "MB")
        self.assertEqual(tax.provinces[4], "ON")
        self.assertEqual(tax.provinces[5], "QC")
        self.assertEqual(tax.provinces[6], "NB")
        self.assertEqual(tax.provinces[7], "PE")
        self.assertEqual(tax.provinces[8], "NS")
        self.assertEqual(tax.provinces[9], "NL")
        pass

    def test_init(self):
        tax = taxes()
        self.assertEqual(tax.location, "ON")
        self.assertEqual(tax.federal_tax_brackets.top_bracket_tax_rate, 0.33)
        self.assertEqual(tax.federal_tax_brackets.brackets[0].income, 98040)
        self.assertEqual(tax.federal_tax_brackets.brackets[0].bracket_size, 98040)
        self.assertEqual(tax.federal_tax_brackets.brackets[0].tax_rate, 0.205)
        self.assertEqual(tax.federal_tax_brackets.brackets[1].income, 151978)
        self.assertEqual(tax.federal_tax_brackets.brackets[1].bracket_size, 151978-98040)
        self.assertEqual(tax.federal_tax_brackets.brackets[1].tax_rate, 0.26)
        self.assertEqual(tax.federal_tax_brackets.brackets[2].income, 216511)
        self.assertEqual(tax.federal_tax_brackets.brackets[2].bracket_size, 216511-151978)
        self.assertEqual(tax.federal_tax_brackets.brackets[2].tax_rate, 0.2932)

        self.assertEqual(tax.provincial_tax_brackets["ON"].top_bracket_tax_rate, 0.1316)
        self.assertEqual(tax.provincial_tax_brackets["ON"].brackets[0].income, 45142)
        self.assertEqual(tax.provincial_tax_brackets["ON"].brackets[0].bracket_size, 45142)
        self.assertEqual(tax.provincial_tax_brackets["ON"].brackets[0].tax_rate, 0.0505)
        self.assertEqual(tax.provincial_tax_brackets["ON"].brackets[1].income, 90287)
        self.assertEqual(tax.provincial_tax_brackets["ON"].brackets[1].bracket_size, 90287-45142)
        self.assertEqual(tax.provincial_tax_brackets["ON"].brackets[1].tax_rate, 0.0915)
        self.assertEqual(tax.provincial_tax_brackets["ON"].brackets[2].income, 150000)
        self.assertEqual(tax.provincial_tax_brackets["ON"].brackets[2].bracket_size, 150000-90287)
        self.assertEqual(tax.provincial_tax_brackets["ON"].brackets[2].tax_rate, 0.1116)
        self.assertEqual(tax.provincial_tax_brackets["ON"].brackets[3].income, 220000)
        self.assertEqual(tax.provincial_tax_brackets["ON"].brackets[3].bracket_size, 220000-150000)
        self.assertEqual(tax.provincial_tax_brackets["ON"].brackets[3].tax_rate, 0.1216)

    def test_set_location(self):
        tax = taxes()
        tax.set_location("BC")
        self.assertEqual(tax.location, "BC")
        tax.set_location("AB")
        self.assertEqual(tax.location, "AB")
        tax.set_location("SK")
        self.assertEqual(tax.location, "SK")
        tax.set_location("MB")
        self.assertEqual(tax.location, "MB")
        tax.set_location("ON")
        self.assertEqual(tax.location, "ON")
        tax.set_location("QC")
        self.assertEqual(tax.location, "QC")
        tax.set_location("NB")
        self.assertEqual(tax.location, "NB")
        tax.set_location("PE")
        self.assertEqual(tax.location, "PE")
        tax.set_location("NS")
        self.assertEqual(tax.location, "NS")
        tax.set_location("NL")
        self.assertEqual(tax.location, "NL")

    def test_set_location_fail(self):
        tax = taxes()
        with self.assertRaises(Exception) as context:
            tax.set_location("BADLOC")
        #print ("\n%s" % str(context.exception))
        self.assertTrue(("Location 'BADLOC' invalid, not one of BC,AB,SK,MB,"
                         "ON,QC,NB,PE,NS,NL") in str(context.exception))

    def test_max_combined_tax_rate(self):
        tax = taxes()
        max_rate = tax._max_combined_tax_rate()
        self.assertEqual(max_rate, 0.1316+.33)

    def test_compute_taxes(self):
        tax = taxes()
        tot_tax = tax.compute_taxes(1000)
        self.assertEqual(tot_tax, 255.5)

    def test_gross_income_for_net_income(self):
        tax = taxes()
        gross, tot_tax = tax.gross_income_for_net_income(50000)
        self.assertEqual(gross, 68442.33)
        self.assertEqual(tot_tax, 18442.33)

        gross, tot_tax = tax.gross_income_for_net_income(150000)
        self.assertEqual(gross, 230737.25)
        self.assertEqual(tot_tax, 80737.25)
