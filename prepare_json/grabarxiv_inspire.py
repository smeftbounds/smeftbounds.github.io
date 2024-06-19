#!/usr/bin/env python3
"""
Simple Python3 script to look up citations on the
Inspirehep database (https://inspirehep.net/).
"""

__author__ = 'Anke Biekoetter'
__email__ = 'biekoetter@uni-mainz.de'

import argparse
import sys

#import urllib.request
import re
import requests

parser = argparse.ArgumentParser()
parser.add_argument("input", nargs='+', help="Name(s)/path(s) of input tex-file(s).")
parser.add_argument("--format", '-f', default='bibtex', help="Format in which citations are fetched: " +
                                                                           "Bibtex -- bibtex " +
                                                                           "Latex EU -- latex-eu")
args = parser.parse_args()


# fetch the data
def fetch_inspire(icd, format):
    print("Fetching {}".format(icd))
    url = 'https://inspirehep.net/api/literature?q={}&format={}'.format(icd, format)
    print(url)
    url = 'https://inspirehep.net/api/arxiv/'+icd+'&format=authors'
    print(url)
    bibfetch = requests.get(url)
    print(bibfetch.content)

    bibentry = str(bibfetch.content, 'utf8', errors='replace')

    return bibentry

#def write_bib(ofname):
#    citationkeys = fetch_latex(args.input)
#    with open(ofname, 'w') as bibfile:
#        for key in citationkeys:
#            bibentry = fetch_inspire(key, args.format)
#            print(bibentry, file=bibfile)
#
#    bibfile.close()
#
#    print("Done.")
#    return 0

# take filename from infile
#outfilename = '{}.bib'.format(args.input[0][:-4])
arXivID = args.input[0]
print(arXivID)
fetch_inspire(arXivID, args.format)
#write_bib(outfilename)
