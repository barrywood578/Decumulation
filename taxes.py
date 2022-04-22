#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
    Compute income taxes for Ontario.
"""

from optparse import OptionParser
import sys
import os
import logging

class tax_bracket(object):
    def __init__(self, income, tax_rate, lower_bracket=None):
        self.income       = income
        self.bracket_size = income
        self.tax_rate     = tax_rate
        if lower_bracket is not None:
            self.bracket_size = self.bracket_size - lower_bracket

class tax_brackets(object):
    def __init__(self, top_bracket_tax_rate):
        self.brackets = [ ]
        self.top_bracket_tax_rate = top_bracket_tax_rate

    def set_top_bracket_rate(self, top_bracket_tax_rate):
        self.top_bracket_tax_rate = top_bracket_tax_rate

    def add_bracket(self, income, tax_rate):
        prev_income = None
        for index, bracket in enumerate(self.brackets):
            if bracket.income < income:
               prev_income = bracket.income
               continue
            if bracket.income == income:
                self.brackets[index].tax_rate = tax_rate
                return
            # Reached bracket of higher income
            self.brackets.insert(index, tax_bracket(income, tax_rate, prev_income))
            self.brackets[index+1].bracket_size = (self.brackets[index+1].income
                                                - income)
            return
        self.brackets.extend([tax_bracket(income, tax_rate, prev_income)])

    def compute_tax(self, income):
        tax = 0.0
        remainder = income
        for bracket in self.brackets:
            if income <= bracket.income:
                tax += (remainder * bracket.tax_rate)
                remainder = 0
                break
            tax += (bracket.tax_rate * bracket.bracket_size)
            remainder -= bracket.bracket_size
        tax = tax + (remainder * self.top_bracket_tax_rate)
        return tax

class taxes(object):
    provinces = ["BC", "AB", "SK", "MB", "ON", "QC", "NB", "PE", "NS", "NL"]

    def __init__(self):
        self.location = "ON"

        self.federal_tax_brackets = tax_brackets( 0.33 )
        self.federal_tax_brackets.add_bracket( 98040, 0.205 )
        self.federal_tax_brackets.add_bracket( 151978, 0.26  )
        self.federal_tax_brackets.add_bracket( 216511, 0.2932)

        self.provincial_tax_brackets = { }
        for prov in self.provinces:
            self.provincial_tax_brackets[prov] = tax_brackets(0)
        self.provincial_tax_brackets["ON"].add_bracket(45142, 0.0505)
        self.provincial_tax_brackets["ON"].add_bracket(90287, 0.0915)
        self.provincial_tax_brackets["ON"].add_bracket(150000, 0.1116)
        self.provincial_tax_brackets["ON"].add_bracket(220000, 0.1216)
        self.provincial_tax_brackets["ON"].set_top_bracket_rate(0.1316)
                                                               
    def set_location(self, location):
        if location in self.provinces:
            self.location = location
            return
        raise ValueError("Location '%s' invalid, not one of %s" %
                         (location, ",".join(self.provinces)))

    def _federal_taxes(self, income):
        return self.federal_tax_brackets.compute_tax(income)

    def _provincial_taxes(self, income):
        return self.provincial_tax_brackets[self.location].compute_tax(income)

    def _max_combined_tax_rate(self):
        max_fed = self.federal_tax_brackets.top_bracket_tax_rate
        max_prov = self.provincial_tax_brackets[self.location].top_bracket_tax_rate
        return max_fed + max_prov

    def compute_taxes(self, income=0.0):
        if income <= 0:
            return 0.0
        fed_taxes = round(self._federal_taxes(income), 2)
        prov_taxes = round(self._provincial_taxes(income), 2)
        return round(fed_taxes + prov_taxes, 2)

    def gross_income_for_net_income(self, net_income):
        low_gross = net_income
        high_gross = net_income / (1-self._max_combined_tax_rate())
        mid_gross = (low_gross + high_gross)/2

        taxes = self.compute_taxes(mid_gross)
        while (abs(mid_gross - taxes - net_income) > 0.01):
            ## Mid gross is too low, bump it up
            if (mid_gross - taxes) < net_income:
                low_gross = mid_gross
            else:
            ## Mid gross is too high, bump it down
                high_gross = mid_gross
            mid_gross = (low_gross + high_gross)/2
            taxes = self.compute_taxes(mid_gross)

        return round(mid_gross,2), round(taxes, 2)

def create_parser():
    parser = OptionParser(description="Quick check for tax computation.")
    parser.add_option('-i', '--income',
            dest = 'income',
            action = 'store', type = 'float', default = 1000.0,
            help = 'Compute taxes for this income.',
            metavar = 'Income')
    return parser

def main(argv = None):
    logging.basicConfig(level=logging.INFO)
    parser = create_parser()
    if argv is None:
        argv = sys.argv[1:]

    (options, argv) = parser.parse_args(argv)
    if len(argv) != 0:
        print('Must enter income!')
        print
        parser.print_help()
        return -1

    obj = taxes()
    all_taxes = obj.compute_taxes(income=options.income)
    print("Gross In  : %8.2f" % options.income)
    print("Taxes     : %8.2f" % all_taxes)
    print("Net Income: %8.2f\n" % (options.income - all_taxes))

    gross, tot_tax = obj.gross_income_for_net_income(options.income)
    comp_tax = obj.compute_taxes(gross)
    print("Target Net: %8.2f" % options.income)
    print("Gross4Net : %8.2f" % gross)
    print("Taxes     : %8.2f" % tot_tax)
    print("Tax Check : %8.2f" % comp_tax)
    print("Net Income: %8.2f" % (gross - tot_tax))

if __name__ == '__main__':
    sys.exit(main())
