#!/usr/bin/env python3
"""
Simple Python3 script to look up citations on the
Inspirehep database (https://inspirehep.net/).
"""

__author__ = 'Sebastian Schenk'
__email__ = 'sebastian.schenk@durham.ac.uk'

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

# read the latex file
def fetch_latex(fnames):
    ftex = ''
    for fname in fnames:
        infile = open(fname)
        ftex += infile.read()
        infile.close()
    citesraw = re.findall('cite{(.+?)}', ftex)

    # split the matching patterns and strip off whitespace
    citesraw = [n.split(',') for n in citesraw]
    citesdupl = [item.strip() for sublist in citesraw for item in sublist]
    # remove duplicates
    # preserve order
    seen = set()
    citationkeys = []
    for item in citesdupl:
        if item not in seen:
            seen.add(item)
            citationkeys.append(item)

    return citationkeys

# fetch the data
def fetch_inspire(icd, format):
    print("Fetching {}".format(icd))
    url = 'https://inspirehep.net/api/literature?q={}&format={}'.format(icd, format)
    bibfetch = requests.get(url)
    bibentry = str(bibfetch.content, 'utf8', errors='replace')

    return bibentry

def write_bib(ofname):
    citationkeys = fetch_latex(args.input)
    with open(ofname, 'w') as bibfile:
        for key in citationkeys:
            bibentry = fetch_inspire(key, args.format)
            print(bibentry, file=bibfile)

    bibfile.close()

    print("Done.")
    return 0

# take filename from infile
outfilename = '{}.bib'.format(args.input[0][:-4])
write_bib(outfilename)
