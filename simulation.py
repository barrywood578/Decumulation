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
        self.assets = []
        self.taxes = taxes()

    def add_asset(self, cost, range_min, range_max, income_min, income_max,
                  curr_value=None, salary=None):
        asset = assets(cost, range_min, range_max, curr_value)
        asset.set_income_range(income_min, income_max, salary)
        self.assets.append(asset)

    def run_one_interval(self):
        income = 0
        for asset in self.assets:
            asset.update_value()
            income += asset.generate_income()
        fed, prov = self.taxes.compute_taxes(income)
        return income, fed, prov

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

    sim = simulation()
    sim.add_asset(options.cost, options.min_infl, options.max_infl, 
            options.min_infl/10.0, options.max_infl/10.0,
            options.value, options.cost/10.0)
    print("Yr |   Income |  Fed Tax | Prov Tax | Net Income")
    for year in range(1,10):
        income, fed, prov = sim.run_one_interval()
        print("%2d | %8.2f | %8.2f | %8.2f | %8.2f" % (
               year, income, fed, prov, income -fed - prov))

    print("Current value: %8.2f" % sim.assets[0].current_value)

if __name__ == '__main__':
    sys.exit(main())
