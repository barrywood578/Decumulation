#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
    Simulation: Run asset for 30 years, computing income and taxes
"""

from optparse import OptionParser
import sys
import os
import logging
from assets import *
from taxes import *

class simulation(object):
    def __init__(self):
        self.asset = None
        self.taxes = taxes()

    def add_asset(self, cost, range_min, range_max, income_min, income_max,
                  curr_value=None, salary=None):
        self.asset = assets(cost, range_min, range_max, curr_value)
        self.asset.set_income_range(income_min, income_max, salary)

    def run_one_interval(self, after_tax_income):
        gross_income, stuff = self.taxes.gross_income_for_net_income(after_tax_income)
        self.asset.update_value(add_income=True)
        self.asset.generate_income()
        actual_income = self.asset.take_profit(gross_income)
        actual_taxes = self.taxes.compute_taxes(actual_income)
        return gross_income, actual_income, actual_taxes

def create_parser():
    parser = OptionParser(description="Quick check for asset computation.")
    parser.add_option('-c', '--cost',
            dest = 'cost',
            action = 'store', type = 'float', default = 1000.0,
            help = 'Asset cost.',
            metavar = 'Cost')
    parser.add_option('-v', '--value',
            dest = 'value',
            action = 'store', type = 'float', default = None,
            help = 'Asset current value.',
            metavar = 'Value')
    parser.add_option('-m', '--min_infl',
            dest = 'min_infl',
            action = 'store', type = 'float', default = 1.0,
            help = 'Minimum inflation factor.',
            metavar = 'Min_delta')
    parser.add_option('-M', '--max_infl',
            dest = 'max_infl',
            action = 'store', type = 'float', default = 1.0,
            help = 'Maximum inflation factor.',
            metavar = 'Max_delta')
    parser.add_option('-i', '--income',
            dest = 'income',
            action = 'store', type = 'float', default = 100.0,
            help = 'Desired yearly income.',
            metavar = 'Income')
    return parser

def main(argv = None):
    logging.basicConfig(level=logging.INFO)
    parser = create_parser()
    if argv is None:
        argv = sys.argv[1:]

    (options, argv) = parser.parse_args(argv)
    if len(argv) != 0:
        print('Must enter cost!')
        print
        parser.print_help()
        return -1

    sim = simulation()
    sim.add_asset(options.cost, options.min_infl, options.max_infl, 
            options.min_infl, options.max_infl)
    print("Current value: %8.2f" % sim.asset.current_value)
    print("Yr | GrossInc |   Income |   Taxes  | Net Income | CurrValue")
    for year in range(1,10):
        gross_income, income, taxes = sim.run_one_interval(options.income)
        print("%2d | %8.2f | %8.2f | %8.2f | %8.2f   | %8.2f" % (
               year, gross_income, income, taxes, income - taxes, sim.asset.current_value))
        if sim.asset.worthless():
            print("You're broke!")
            break


if __name__ == '__main__':
    sys.exit(main())
