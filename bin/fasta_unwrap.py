#!/usr/bin/env python

"""
fasta_unwrap.py: hard-wrapped fastas unwrapped (sequence is just 1 line)

Usage:
  fasta_unwrap.py <fasta> | [-]
  fasta_unwrap.py -h | --help
  fasta_unwrap.py --version

Options:
  <fasta>       Fasta file name ('-' if from STDIN).
  -h --help     Show this screen.
  --version     Show version.

Description:
  Simply unwrap a hard-wrapped fasta file
"""

from docopt import docopt

if __name__ == '__main__':
    args = docopt(__doc__, version='0.1')

import sys
import fileinput
import re

# fixing broken pipe error
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL) 

# IO error
if args['<fasta>'] is None:
    sys.stderr.write('Provide fasta via arg or STDIN')
    sys.stderr.write(__doc__)
    sys.exit()


if args['<fasta>'] == '-':
    inf = sys.stdin
else: 
    inf = open(args['<fasta>'], 'r')


# parsing fasta
line_cnt = 0
for line in inf:
    line_cnt += 1
    if line.startswith('>'):
        if line_cnt > 1:
            print ''
        sys.stdout.write(line)
    else:
        sys.stdout.write(line.rstrip())
