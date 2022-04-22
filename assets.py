#!/usr/bin/env python
# -*- coding: latin-1 -*-
"""
    Asset management base class
"""

from optparse import OptionParser
import sys
import os
import logging
import random

class assets(object):
    def __init__(self, cost, range_min, range_max, curr_value=None):
        self.cost = cost
        self.current_value = cost
        if curr_value is not None:
            self.current_value = curr_value
        self.range_min = range_min
        self.range_max = range_max
        self.salary = None
        self.income_min = 0
        self.income_max = 0
        self.income_bank = 0

    def update_value(self, add_income=False):
        delta = random.uniform(self.range_min, self.range_max)
        if add_income:
            self.current_value += self.income_bank
            self.income_bank = 0
        self.current_value += self.current_value * delta


    def set_income_range(self, income_min, income_max, salary=None ):
        self.income_min = income_min
        self.income_max = income_max
        if salary is not None:
            self.salary = salary

    def generate_income(self):
        income = 0
        random_factor = random.uniform(self.income_min, self.income_max)
        if self.salary is None:
            income = self.current_value * random_factor
        else:
            income = self.salary * random_factor
        self.income_bank += income
        return income

    def take_profit(self, profit):
        if profit <= self.income_bank:
            self.income_bank -= profit
            return profit
        profit_taken = self.income_bank
        capital_redemption = profit - self.income_bank
        self.income_bank = 0
        if capital_redemption <= self.current_value:
            self.current_value -= capital_redemption
            return profit
        profit_taken += self.current_value
        self.current_value = 0
        return profit_taken

    def worthless(self):
        no_assets = (self.current_value == 0) and (self.income_bank == 0)
        salary = self.salary is not None
        return no_assets and not salary

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

    asset_1 = assets(options.cost, options.min_infl, options.max_infl, options.value)
    asset_1.set_income_range(options.min_infl/10.0, options.max_infl/10.0,
                             options.cost/10.0)
    asset_1.update_value()
    income = asset_1.generate_income()

    print("Asset:\nCost  : %8.2f\nValue : %8.2f\nIncome: %8.2f\n" %
            (asset_1.cost, asset_1.current_value, income))

if __name__ == '__main__':
    sys.exit(main())
