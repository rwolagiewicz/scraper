#!/usr/bin/env python3

#   command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--url', required=True,
                    help='Tested application url')
v = parser.parse_args()

from api import APITester
tested_urls = ['https://www.google.pl/', 'https://arxiv.org/', 'https://www.python.org/']
tester = APITester(v.url)
tester.run_tests(tested_urls)
